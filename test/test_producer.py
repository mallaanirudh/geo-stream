import asyncio

from aiokafka import AIOKafkaProducer


async def main():
    producer = AIOKafkaProducer(
        bootstrap_servers="localhost:29092"
    )

    await producer.start()

    try:
        await producer.send_and_wait(
            "telemetry",
            b"Hello Kafka!"
        )
        print("Message sent!")
    finally:
        await producer.stop()


asyncio.run(main())