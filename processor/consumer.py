from aiokafka import AIOKafkaConsumer
from shared.models import Telemetry
from processor.db import insert_telemetry


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
        print("CONSUMER: waiting for messages...")

        async for message in self.consumer:
         print("CONSUMER: MESSAGE RECEIVED")

         telemetry = Telemetry.model_validate_json(message.value)

         print("CONSUMER: parsed telemetry:", telemetry)

         insert_telemetry(telemetry)

         print("CONSUMER: INSERTED INTO DB")

         yield telemetry
        # async for message in self.consumer:
            # telemetry = Telemetry.model_validate_json(message.value)

            # print(telemetry)

            # insert_telemetry(telemetry)

            # yield telemetry