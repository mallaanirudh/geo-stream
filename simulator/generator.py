import asyncio

from config import UPDATE_INTERVAL

BATCH_SIZE = 500


class TelemetryGenerator:
    def __init__(self, devices, producer):
        self.devices = devices
        self.producer = producer

    async def start(self):
        while True:
            sent = 0

            for i in range(0, len(self.devices), BATCH_SIZE):
                batch = self.devices[i:i + BATCH_SIZE]

                tasks = []

                for device in batch:
                    telemetry = device.update()
                    tasks.append(self.producer.publish(telemetry))

                await asyncio.gather(*tasks)

                sent += len(batch)

            print(f"Published {sent} events")

            await asyncio.sleep(UPDATE_INTERVAL)