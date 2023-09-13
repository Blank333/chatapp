from chatuser.models import ChatUser, UserInterest
from chatuser.serializers import ChatUserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from django.db import models

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register(request):
    try:
        print(request.data)  # Print the request data for debugging

        serializer = ChatUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully', 'user_email': user.email}, status=status.HTTP_201_CREATED)
        return Response({'Error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as error:
        return Response({'Error': error}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, username=email, password=password)

        if user:
            user.is_online = True
            user.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response('Successfully logged in.', status=status.HTTP_200_OK, headers={'Authorization': f'Token {token.key}'})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_online(request):
    try:
        users = ChatUser.objects.filter(
            is_online=True).values('id', 'email', 'name', 'age')

        if users:
            return Response(users, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No online users found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def suggested_friends(request, user_id):
    try:
        user = ChatUser.objects.get(id=user_id)
        user_interests = UserInterest.objects.filter(user=user)

        similar_users = []

        for interest in user_interests:
            related_users = UserInterest.objects.filter(
                interest=interest.interest, preference_score__gte=interest.preference_score).exclude(user=user)
            for related_user in related_users:
                if related_user.user not in similar_users:
                    similar_users.append(related_user.user)

        recommended_friends = sorted(similar_users, key=lambda x: x.userinterest_set.aggregate(
            max_score=models.Max('preference_score'))['max_score'], reverse=True)[:5]

        recommended_friends_data = []

        for friend in recommended_friends:
            friend_interests_data = []

            for interest in user_interests:
                friend_interest = UserInterest.objects.filter(
                    user=friend, interest=interest.interest).first()
                if friend_interest:
                    similarity_score = min(
                        interest.preference_score, friend_interest.preference_score)
                    friend_interests_data.append({
                        'interest_name': interest.interest.name,
                        'similarity_score': similarity_score
                    })

            recommended_friends_data.append({
                'user_id': friend.id,
                'name': friend.name,
                'age': friend.age,
                'interests': friend_interests_data
            })

        return Response({'recommended_friends': recommended_friends_data}, status=status.HTTP_200_OK)

    except ChatUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
