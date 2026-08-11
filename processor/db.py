import os
import psycopg
from dotenv import load_dotenv
from shared.models import Telemetry

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set")


def test_connection():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version();")
            result = cur.fetchone()
            print("Connected to PostgreSQL!")
            print(result[0])

def create_tables():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:

            cur.execute("""
                CREATE TABLE IF NOT EXISTS telemetry (
                    timestamp TIMESTAMPTZ NOT NULL,
                    device_id INTEGER NOT NULL,
                    latitude DOUBLE PRECISION NOT NULL,
                    longitude DOUBLE PRECISION NOT NULL,
                    speed DOUBLE PRECISION NOT NULL,
                    temperature DOUBLE PRECISION NOT NULL,
                    battery DOUBLE PRECISION NOT NULL
                );
            """)

            cur.execute("""
                SELECT create_hypertable(
                    'telemetry',
                    by_range('timestamp'),
                    if_not_exists => TRUE
                );
            """)

        conn.commit()

    print("Telemetry hypertable created successfully!")
def insert_telemetry(telemetry: Telemetry):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
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
                (
                    telemetry.timestamp,
                    telemetry.device_id,
                    telemetry.latitude,
                    telemetry.longitude,
                    telemetry.speed,
                    telemetry.temperature,
                    telemetry.battery,
                ),
            )

        conn.commit()
if __name__ == "__main__":
    test_connection()
    create_tables()