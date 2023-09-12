from chatuser.models import ChatUser, UserInterest
from chatuser.serializers import ChatUserSerializer, LoginSerializer
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authtoken.models import Token


@api_view(['POST'])
def register(request):
    try:
        serializer = ChatUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
            is_online=True).values('id', 'name', 'age')

        if users:
            res = {}
            for user in users:
                user_interests = UserInterest.objects.filter(
                    user_id=user['id']).values('interest', 'preference_score')

                user['interests'] = user_interests
                res[user['name']] = user

            return Response(res, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No online users found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(res)