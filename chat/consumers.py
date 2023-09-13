import json
from channels.generic.websocket import AsyncWebsocketConsumer
from chatuser.models import Message, ChatUser
from channels.db import database_sync_to_async


class ChatSocketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        receiver_email = data.get('receiver_email')
        message_content = data.get('message_content')

        if not (receiver_email and message_content):
            await self.send(text_data=json.dumps({'error': 'Both receiver_email and message_content are required.'}))
            return

        try:
            sender_email = self.scope['user'].email
            sender = await self.get_chat_user(sender_email)
            receiver = await self.get_chat_user(receiver_email)

            if sender and receiver:
                await self.create_message(sender, receiver, message_content)
                await self.send(text_data=json.dumps({'message': 'Message sent successfully.'}))
            else:
                await self.send(text_data=json.dumps({'error': 'Invalid sender or receiver email.'}))

        except Exception as e:
            await self.send(text_data=json.dumps({'error': str(e)}))

    @database_sync_to_async
    def get_chat_user(self, email):
        try:
            return ChatUser.objects.get(email=email)
        except ChatUser.DoesNotExist:
            return None

    @database_sync_to_async
    def create_message(self, sender, receiver, content):
        Message.objects.create(
            sender=sender, receiver=receiver, content=content)
