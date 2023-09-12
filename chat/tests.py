from django.test import TestCase
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatSocketConsumer


class ChatSocketConsumerTest(TestCase):
    async def test_chat_socket_consumer(self):
        communicator = WebsocketCommunicator(
            ChatSocketConsumer.as_asgi(), "send/")
        connected, _ = await communicator.connect()

        self.assertTrue(connected)

        # Send a message to the consumer
        await communicator.send_json_to({"message": "Test Message"})

        # Receive a message from the consumer
        response = await communicator.receive_json_from()

        # Check if the received message is correct
        self.assertEqual(response, {"message": "Test Message"})

        # Disconnect from the consumer
        await communicator.disconnect()
