from rest_framework.test import APITestCase
from rest_framework import status
from chatuser.models import ChatUser, Interest, UserInterest
from chatuser.serializers import ChatUserSerializer
import json


class RegisterTests(APITestCase):

    def setUp(self):
        Interest.objects.create(name='dancing')
        Interest.objects.create(name='coding')
        Interest.objects.create(name='cars')
        Interest.objects.create(name='sports')

        self.register_url = '/api/register/'

    def test_register_success(self):
        data = {
            'email': 'test1@example.com',
            'password': 'testingpassword',
            'name': 'testuser',
            'age': '28',
            'interests': [
                    {'name': 'dancing', 'preference_score': 24},
                    {'name': 'cars', 'preference_score': 43},
                    {'name': 'coding', 'preference_score': 56},
            ]
        }
        response = self.client.post(
            self.register_url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'message': 'User registered successfully', 'user_email': 'test1@example.com'})
        user = ChatUser.objects.get(email=response.data['user_email'])
        interests = UserInterest.objects.filter(user=user)
        self.assertEqual(len(interests), 3)

    def test_register_interest_len(self):
        data1 = {
            'email': 'test2@example.com',
            'password': 'testingpassword',
            'name': 'testuser',
            'age': '28',
            'interests': [
                    {'name': 'cars', 'preference_score': 43},
                    {'name': 'coding', 'preference_score': 56},
            ]
        }
        data2 = {
            'email': 'test3@example.com',
            'password': 'testingpassword',
            'name': 'testuser',
            'age': '28',
            'interests': [
                    {'name': 'cars', 'preference_score': 43},
                    {'name': 'coding', 'preference_score': 56},
                    {'name': 'coding', 'preference_score': 56},
                    {'name': 'coding', 'preference_score': 56},
                    {'name': 'coding', 'preference_score': 56},
                    {'name': 'coding', 'preference_score': 56},
                    {'name': 'coding', 'preference_score': 56},

            ]
        }
        response = self.client.post(
            self.register_url, data=json.dumps(data1), content_type='application/json')
        serializer = ChatUserSerializer(data=data1)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(serializer.is_valid())
        self.assertIn('interests', serializer.errors)
        self.assertEqual(
            serializer.errors['interests'][0], "You must select between 3 and 6 interests.")

        response = self.client.post(
            self.register_url, data=json.dumps(data2), content_type='application/json')
        serializer = ChatUserSerializer(data=data2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(serializer.is_valid())
        self.assertIn('interests', serializer.errors)
        self.assertEqual(
            serializer.errors['interests'][0], "You must select between 3 and 6 interests.")

    def test_register_interest_invalid(self):
        data = {
            'email': 'test1@example.com',
            'password': 'testingpassword',
            'name': 'testuser',
            'age': '28',
            'interests': [
                    {'name': 'dancing', 'preference_score': 24},
                    {'name': 'cars', 'preference_score': 43},
                    {'name': 'hiking', 'preference_score': 56},
            ]
        }
        response = self.client.post(
            self.register_url, data=json.dumps(data), content_type='application/json')
        serializer = ChatUserSerializer(data=data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(serializer.is_valid())
        self.assertIn('interests', serializer.errors)
        self.assertEqual(
            serializer.errors['interests'][0], "One or more selected interests do not exist.")


class LoginTests(APITestCase):
    def setUp(self):

        ChatUser.objects.create_user(
            name='testuser',
            email='test@example.com',
            password='testingpassword',
            age='28'
        )
        self.login_url = '/api/login/'

    def test_login_success(self):
        response = self.client.post(
            self.login_url, {'email': 'test@example.com', 'password': 'testingpassword'})
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Authorization', response.headers)

    def test_login_invalid_credentials(self):
        response = self.client.post(
            self.login_url, {'email': 'test@example.com', 'password': 'wrongpassword'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.data)

    def test_login_invalid_data(self):
        response = self.client.post(
            self.login_url, {'email': 'wrong@example', 'password': 'testingpassword'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_missing_fields(self):
        response = self.client.post(
            self.login_url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OnlineUsersTests(APITestCase):
    def setUp(self):
        ChatUser.objects.create_user(
            name='testuserOnline1',
            email='test@example.com',
            password='testingpassword',
            age='28',
            is_online=True
        )
        ChatUser.objects.create_user(
            name='testuserOnline2',
            email='test2@example.com',
            password='testingpassword',
            age='28',
            is_online=True
        )
        ChatUser.objects.create_user(
            name='testuserOffline',
            email='test3@example.com',
            password='testingpassword',
            age='28',
        )

    def test_get_online_users(self):
        response = self.client.get('/api/online-users/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        self.assertEqual(response.data[0]['name'], 'testuserOnline1')
        self.assertEqual(response.data[1]['name'], 'testuserOnline2')

    def test_get_no_online_users(self):
        ChatUser.objects.all().update(is_online=False)

        response = self.client.get('/api/get_online/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
