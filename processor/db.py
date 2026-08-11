import os
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

from shared.models import Telemetry

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


pool = AsyncConnectionPool(
    conninfo=DATABASE_URL,
    min_size=2,
    max_size=10,
    open=False,
)


async def start_db():
    await pool.open()
    print("DATABASE: connection pool started")


async def stop_db():
    await pool.close()
    print("DATABASE: connection pool closed")


async def insert_telemetry_batch(telemetries: list[Telemetry]):

    if not telemetries:
        return

    rows = [
        (
            telemetry.timestamp,
            telemetry.device_id,
            telemetry.latitude,
            telemetry.longitude,
            telemetry.speed,
            telemetry.temperature,
            telemetry.battery,
        )
        for telemetry in telemetries
    ]

    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.executemany(
                """
                INSERT INTO telemetry (
                    timestamp,
                    device_id,
                    latitude,
                    longitude,
                    speed,
                    temperature,
                    battery
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                rows,
            )

    print(f"DATABASE: inserted batch of {len(rows)}")
