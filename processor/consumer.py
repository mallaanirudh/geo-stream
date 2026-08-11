import asyncio
from aiokafka import AIOKafkaConsumer
from shared.models import Telemetry
from processor.db import insert_telemetry_batch

class KafkaConsumer:
    def __init__(
        self,
        bootstrap_servers: str,
        topic: str,
        group_id: str = "telemetry-processor",
    ):
        self.consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset="latest",
            enable_auto_commit=True,
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def consume(self):

     batch = []

     while True:

        try:
            message = await asyncio.wait_for(
                self.consumer.getone(),
                timeout=0.1
            )

            telemetry = Telemetry.model_validate_json(message.value)

            batch.append(telemetry)

            # Still allow downstream processing
            yield telemetry

            if len(batch) >= 100:
                await insert_telemetry_batch(batch)
                batch.clear()

        except asyncio.TimeoutError:

            if batch:
                await insert_telemetry_batch(batch)
                batch.clear()
        # async for message in self.consumer:
            # telemetry = Telemetry.model_validate_json(message.value)

            # print(telemetry)

            # insert_telemetry(telemetry)

            # yield telemetry