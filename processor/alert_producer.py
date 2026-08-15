import json

from aiokafka import AIOKafkaProducer

from processor.alerts import Alert


class AlertProducer:

    def __init__(self, bootstrap_servers: str):
        self.producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers
        )

    async def start(self):
        await self.producer.start()
        print("ALERT PRODUCER: started")

    async def stop(self):
        await self.producer.stop()
        print("ALERT PRODUCER: stopped")

    async def send(self, alert: Alert):
        data = {
            "device_id": alert.device_id,
            "alert_type": alert.alert_type,
            "message": alert.message,
            "timestamp": alert.timestamp.isoformat(),
            "latitude": alert.latitude,
            "longitude": alert.longitude,
        }

        await self.producer.send_and_wait(
            "alerts",
            json.dumps(data).encode("utf-8"),
        )