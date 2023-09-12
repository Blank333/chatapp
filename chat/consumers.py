import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("dis-connected")

    async def receive(self, text_data):
        print("received")
        data = json.loads(text_data)
        message = data['message']

        # Handle the message and send a response
        await self.send(text_data=json.dumps({'message': message}))
