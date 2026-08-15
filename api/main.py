import asyncio
import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from aiokafka import AIOKafkaConsumer


app = FastAPI()


KAFKA_BOOTSTRAP_SERVERS = "localhost:29092"
ALERT_TOPIC = "alerts"


# Connected WebSocket clients
connected_clients: set[WebSocket] = set()


@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()
    connected_clients.add(websocket)

    print("WEBSOCKET: client connected")

    try:
        while True:
            # Keep connection alive and detect disconnects
            await websocket.receive_text()

    except WebSocketDisconnect:
        connected_clients.discard(websocket)
        print("WEBSOCKET: client disconnected")


async def kafka_alert_consumer():

    consumer = AIOKafkaConsumer(
        ALERT_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id="websocket-alert-consumer",
        auto_offset_reset="latest",
        enable_auto_commit=True,
    )

    await consumer.start()

    print("WEBSOCKET: Kafka consumer started")

    try:

        async for message in consumer:

            alert = json.loads(message.value.decode("utf-8"))

            print(
                f"WEBSOCKET: broadcasting "
                f"{alert['alert_type']} "
                f"device={alert['device_id']}"
            )

            disconnected = set()

            for websocket in connected_clients:

                try:
                    await websocket.send_json(alert)

                except Exception:
                    disconnected.add(websocket)

            connected_clients.difference_update(disconnected)

    finally:
        await consumer.stop()


@app.on_event("startup")
async def startup():

    asyncio.create_task(
        kafka_alert_consumer()
    )


@app.get("/")
async def root():

    return {
        "status": "ok",
        "service": "geospatial telemetry API",
    }