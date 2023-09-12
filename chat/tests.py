from django.test import TestCase
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatSocketConsumer

from rest_framework.test import APITestCase
from rest_framework import status
from chatuser.models import ChatUser


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


class StartChatTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = ChatUser.objects.create_user(
            name='testuser',
            email='test@example.com',
            password='testingpassword',
            age='28'
        )
        self.recipient = ChatUser.objects.create_user(
            name='testuserReceive',
            email='testReceive@example.com',
            password='testingpassword',
            age='28'
        )

        self.login_url = '/api/login/'
        self.client.post(
            self.login_url, {'email': 'testReceive@example.com', 'password': 'testingpassword'})

    def test_start_chat_success(self):
        # Login the user
        response = self.client.post(
            self.login_url, {'email': 'test@example.com', 'password': 'testingpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.headers['Authorization']

        # Set the authentication header
        self.client.credentials(HTTP_AUTHORIZATION=f'{token}')

        # Send a POST request to start a chat
        response = self.client.post(
            '/api/chat/start/', {'recipient_email': 'testReceive@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {'message': 'Chat initiated successfully'})
