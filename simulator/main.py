import asyncio
import random

from config import *
from device import Device
from generator import TelemetryGenerator
from kafka_producer import KafkaProducer


devices = []

for i in range(NUMBER_OF_DEVICES):

    lat = CITY_CENTER["lat"] + random.uniform(-0.02, 0.02)
    lon = CITY_CENTER["lon"] + random.uniform(-0.02, 0.02)

    devices.append(Device(i, lat, lon))


async def main():

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        topic=KAFKA_TOPIC,
    )

    await producer.start()

    generator = TelemetryGenerator(
        devices,
        producer,
    )

    try:
        await generator.start()

    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())