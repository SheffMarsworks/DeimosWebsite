import json
import asyncio
import psutil
from channels.generic.websocket import AsyncWebsocketConsumer

class TelemetryConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.running = True
        asyncio.create_task(self.send_telemetry())

    async def disconnect(self, close_code):
        self.running = False

    async def receive(self, text_data):
        data = json.loads(text_data)
        command = data.get("command")
        print("Received command:", command)

        # Echo back confirmation (so you can see it works)
        await self.send(text_data=json.dumps({
            "status": "received",
            "command": command
        }))

    async def send_telemetry(self):
        while self.running:
            data = {
                "cpu": psutil.cpu_percent(),
                "ram": psutil.virtual_memory().percent,
                "heartbeat": True
            }
            await self.send(text_data=json.dumps(data))
            await asyncio.sleep(0.5)
