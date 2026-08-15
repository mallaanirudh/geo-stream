import asyncio

from aiokafka import AIOKafkaConsumer

from shared.models import Telemetry
from processor.alert_producer import AlertProducer
from processor.db import (
    insert_telemetry_batch,
    insert_alert_batch,
)

from processor.alerts import AlertEngine


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

        self.alert_engine = AlertEngine(
            max_temperature=30.0,
            min_battery=99.0,
            max_speed=35.0,
        )
        self.alert_producer = AlertProducer(
           bootstrap_servers=bootstrap_servers
        )
    async def start(self):
        await self.consumer.start()
        await self.alert_producer.start()

    async def stop(self):
        await self.consumer.stop()
        await self.alert_producer.stop()

    async def consume(self):

        telemetry_batch = []
        alert_batch = []

        while True:

            try:
                message = await asyncio.wait_for(
                    self.consumer.getone(),
                    timeout=0.1,
                )

                # Convert Kafka message → Telemetry
                telemetry = Telemetry.model_validate_json(
                    message.value
                )
                alerts = self.alert_engine.check(telemetry)

                for alert in alerts:
                    print(
                        f"ALERT [{alert.alert_type}] "
                        f"device={alert.device_id} "
                        f"{alert.message}"
                    )
                    alert_batch.append(alert)

                    await self.alert_producer.send(alert)

                alert_batch.extend(alerts)

                telemetry_batch.append(telemetry)

                # Allow downstream processing
                yield telemetry


                if len(telemetry_batch) >= 100:

                    await insert_telemetry_batch(
                        telemetry_batch
                    )

                    telemetry_batch.clear()

                if len(alert_batch) >= 100:

                    await insert_alert_batch(
                        alert_batch
                    )

                    alert_batch.clear()

            except asyncio.TimeoutError:

                # Flush remaining telemetry
                if telemetry_batch:

                    await insert_telemetry_batch(
                        telemetry_batch
                    )

                    telemetry_batch.clear()

                # Flush remaining alerts
                if alert_batch:

                    await insert_alert_batch(
                        alert_batch
                    )

                    alert_batch.clear()