"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";

const Map = dynamic(() => import("./Map"), {
  ssr: false,
});

type Alert = {
  device_id: number;
  alert_type: string;
  message: string;
  timestamp: string;
  latitude: number;
  longitude: number;
};

export default function Home() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/alerts");

    ws.onopen = () => {
      console.log("WebSocket connected");
      setConnected(true);
    };

    ws.onmessage = (event) => {
      const alert: Alert = JSON.parse(event.data);

      setAlerts((prev) => [alert, ...prev].slice(0, 50));
    };

    ws.onclose = () => {
      setConnected(false);
    };

    return () => ws.close();
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-white p-6">

      <h1 className="text-3xl font-bold mb-6">
        GeoStream Monitor
      </h1>

      <div className="grid grid-cols-3 gap-4 mb-6">

        <div className="bg-slate-900 rounded-xl p-5">
          <p className="text-slate-400">System</p>
          <p className="text-xl font-bold">
            {connected ? "🟢 Connected" : "🔴 Disconnected"}
          </p>
        </div>

        <div className="bg-slate-900 rounded-xl p-5">
          <p className="text-slate-400">Alerts</p>
          <p className="text-2xl font-bold">
            {alerts.length}
          </p>
        </div>

        <div className="bg-slate-900 rounded-xl p-5">
          <p className="text-slate-400">Devices</p>
          <p className="text-2xl font-bold">
            10,000+
          </p>
        </div>

      </div>

      <div className="grid grid-cols-3 gap-6">

        <div className="col-span-2 bg-slate-900 rounded-xl overflow-hidden">
          <div className="p-4 font-semibold">
            Live Device Map
          </div>

          <Map alerts={alerts} />
        </div>

        <div className="bg-slate-900 rounded-xl p-4">

          <h2 className="font-semibold mb-4">
            Live Alerts
          </h2>

          <div className="space-y-3 max-h-[600px] overflow-y-auto">

            {alerts.length === 0 && (
              <p className="text-slate-500">
                Waiting for alerts...
              </p>
            )}

            {alerts.map((alert, index) => (
              <div
                key={index}
                className="border border-slate-700 rounded-lg p-3"
              >

                <div className="flex justify-between">

                  <span className="font-semibold">
                    {alert.alert_type}
                  </span>

                  <span className="text-xs text-slate-500">
                    Device {alert.device_id}
                  </span>

                </div>

                <p className="text-sm text-slate-400 mt-1">
                  {alert.message}
                </p>

              </div>
            ))}

          </div>

        </div>

      </div>

    </main>
  );
}