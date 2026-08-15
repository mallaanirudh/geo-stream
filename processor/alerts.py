from dataclasses import dataclass
from datetime import datetime

from shared.models import Telemetry


@dataclass
class Alert:
    device_id: int
    alert_type: str
    message: str
    timestamp: datetime
    latitude: float
    longitude: float


class AlertEngine:

    def __init__(
        self,
        max_temperature: float = 40.0,
        min_battery: float = 20.0,
        max_speed: float = 80.0,
    ):
        self.max_temperature = max_temperature
        self.min_battery = min_battery
        self.max_speed = max_speed

    def check(self, telemetry: Telemetry) -> list[Alert]:
        alerts = []

        # High temperature
        if telemetry.temperature > self.max_temperature:
            alerts.append(
                Alert(
                    device_id=telemetry.device_id,
                    alert_type="HIGH_TEMPERATURE",
                    message=(
                        f"Temperature {telemetry.temperature:.2f}°C "
                        f"exceeds {self.max_temperature:.2f}°C"
                    ),
                    timestamp=telemetry.timestamp,
                    latitude=telemetry.latitude,
                    longitude=telemetry.longitude,
                )
            )

        # Low battery
        if telemetry.battery < self.min_battery:
            alerts.append(
                Alert(
                    device_id=telemetry.device_id,
                    alert_type="LOW_BATTERY",
                    message=(
                        f"Battery {telemetry.battery:.2f}% "
                        f"is below {self.min_battery:.2f}%"
                    ),
                    timestamp=telemetry.timestamp,
                    latitude=telemetry.latitude,
                    longitude=telemetry.longitude,
                )
            )

        # Overspeed
        if telemetry.speed > self.max_speed:
            alerts.append(
                Alert(
                    device_id=telemetry.device_id,
                    alert_type="OVERSPEED",
                    message=(
                        f"Speed {telemetry.speed:.2f} "
                        f"exceeds {self.max_speed:.2f}"
                    ),
                    timestamp=telemetry.timestamp,
                    latitude=telemetry.latitude,
                    longitude=telemetry.longitude,
                )
            )

        return alerts