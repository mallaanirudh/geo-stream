import asyncio

from device import Device


class TelemetryGenerator:
    def __init__(self, devices):
        self.devices = devices

    async def start(self):
        while True:
            telemetry = []

            for device in self.devices:
                telemetry.append(device.update())

            for event in telemetry[:5]:
                print(event.model_dump_json())

            print(f"Generated {len(telemetry)} events")

            await asyncio.sleep(1)