import asyncio
import random

from config import NUMBER_OF_DEVICES, CITY_CENTER
from device import Device
from generator import TelemetryGenerator


devices = []

for i in range(NUMBER_OF_DEVICES):
    lat = CITY_CENTER["lat"] + random.uniform(-0.02, 0.02)
    lon = CITY_CENTER["lon"] + random.uniform(-0.02, 0.02)

    devices.append(Device(i, lat, lon))


async def main():
    generator = TelemetryGenerator(devices)
    await generator.start()


if __name__ == "__main__":
    asyncio.run(main())