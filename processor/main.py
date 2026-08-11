import asyncio
import selectors
from processor.consumer import KafkaConsumer
from simulator.config import *
from processor.db import start_db, stop_db

async def main():
    await start_db()
    consumer = KafkaConsumer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        topic=KAFKA_TOPIC,
    )

    await consumer.start()

    try:
        print("CONSUMER STARTED - waiting for messages...")
        count = 0
        async for telemetry in consumer.consume():
            count += 1

            if count % 1000 == 0:
               print(f"Processed {count} telemetry messages")

    finally:
        await consumer.stop()
        await stop_db()


if __name__ == "__main__":
    asyncio.run(
        main(),
        loop_factory=lambda: asyncio.SelectorEventLoop(
            selectors.SelectSelector()
        )
    )