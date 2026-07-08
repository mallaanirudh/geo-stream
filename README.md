10,000 Simulated Devices
            │
            ▼
      Kafka Producer
            │
            ▼
     Kafka Topic
      (telemetry)
            │
            ▼
     Kafka Consumer
            │
      ┌─────┴──────┐
      ▼            ▼
TimescaleDB   Alert Engine
                    │
                    ▼
            WebSocket Server
                    │
                    ▼
          Next.js Dashboard
//Add AIOKafkaProducer.send()          