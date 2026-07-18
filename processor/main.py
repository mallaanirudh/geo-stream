import asyncio

from processor.consumer import KafkaConsumer
from simulator.config import *


async def main():

    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        topic=KAFKA_TOPIC,
    )

    await consumer.start()

    try:
        async for telemetry in consumer.consume():
            pass

    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())