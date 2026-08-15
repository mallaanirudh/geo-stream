"use client";

import {
  MapContainer,
  TileLayer,
  CircleMarker,
  Popup,
} from "react-leaflet";

import "leaflet/dist/leaflet.css";

type Alert = {
  device_id: number;
  alert_type: string;
  message: string;
  latitude: number;
  longitude: number;
};

export default function Map({
  alerts,
}: {
  alerts: Alert[];
}) {
  return (
    <MapContainer
      center={[20, 78]}
      zoom={5}
      style={{ height: "600px", width: "100%" }}
    >

      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {alerts.map((alert, index) => (
        <CircleMarker
          key={index}
          center={[
            alert.latitude,
            alert.longitude,
          ]}
          radius={8}
        >
          <Popup>
            <b>{alert.alert_type}</b>
            <br />
            Device: {alert.device_id}
            <br />
            {alert.message}
          </Popup>
        </CircleMarker>
      ))}

    </MapContainer>
  );
}