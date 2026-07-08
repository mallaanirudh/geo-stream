from aiokafka import AIOKafkaProducer
from models import Telemetry


class KafkaProducer:
    def __init__(self, bootstrap_servers: str, topic: str):
        self.topic = topic
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
        )

    async def start(self):
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def publish(self, telemetry: Telemetry):
        await self.producer.send_and_wait(
            topic=self.topic,
            value=telemetry.model_dump_json().encode("utf-8"),
            key=str(telemetry.device_id).encode("utf-8"),
        )