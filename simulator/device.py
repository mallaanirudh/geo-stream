from datetime import datetime, UTC
import random,math

from models import Telemetry


class Device:
    def __init__(self, device_id: int, latitude: float, longitude: float):
        self.device_id = device_id

        self.latitude = latitude
        self.longitude = longitude

        self.speed = random.uniform(20, 60)
        self.temperature = random.uniform(25, 35)
        self.battery = 100.0

        self.heading = random.uniform(0, 360)

    def update(self) -> Telemetry:
        self._update_position()
        self._update_speed()
        self._update_temperature()
        self._update_battery()

        return Telemetry(
            device_id=self.device_id,
            timestamp=datetime.now(UTC),
            latitude=self.latitude,
            longitude=self.longitude,
            speed=self.speed,
            temperature=self.temperature,
            battery=self.battery,
        )
    def _update_position(self):
     self.heading += random.uniform(-8, 8)

     distance = self.speed / 3600

     lat_delta = distance * math.cos(math.radians(self.heading)) / 111

     lon_delta = (
            distance
          * math.sin(math.radians(self.heading))
         / (111 * math.cos(math.radians(self.latitude)))
    )

     self.latitude += lat_delta
     self.longitude += lon_delta
    def _update_battery(self):
     self.battery -= random.uniform(0.005, 0.02)
     self.battery = max(self.battery, 0) 
    def _update_temperature(self):
     self.temperature += random.uniform(-0.3, 0.3)
     self.temperature = max(15, min(self.temperature, 90)) 
    def _update_speed(self):
     self.speed += random.uniform(-5, 5)
     self.speed = max(0, min(self.speed, 120)) 