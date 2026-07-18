from aiokafka import AIOKafkaConsumer
from shared.models import Telemetry


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
        async for message in self.consumer:
            telemetry = Telemetry.model_validate_json(message.value)

            print(telemetry)

            yield telemetry