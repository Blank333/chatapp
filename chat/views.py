from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from chatuser.models import ChatUser
from .serializers import StartChatSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

import json
import websockets


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def start_chat(request):
    try:
        serializer = StartChatSerializer(data=request.data)
        if serializer.is_valid():
            sender_email = request.user.email
            recipient_email = serializer.validated_data.get('recipient_email')
            if sender_email == recipient_email:
                return Response({'error': 'You cannot start a chat with yourself'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                recipient = ChatUser.objects.filter(
                    email=recipient_email).first()

                if not recipient.is_online:
                    return Response({'error': 'Recipient Offline'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
                else:
                    return Response({'message': 'Chat initiated successfully'}, status=status.HTTP_200_OK)
            except:
                return Response({'error': 'Invalid recipient'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# TODO
async def websocket_handler(websocket, path):
    # WebSocket connections

    try:
        async for message in websocket:
            data = json.loads(message)
            receiver_email = data.get('receiver_email')
            message_content = data.get('message_content')

            if not (receiver_email and message_content):
                await websocket.send(json.dumps({'error': 'Both receiver_email and message_content are required.'}))
                continue

            await websocket.send(json.dumps({'message': 'Message sent successfully.'}))

    except Exception as e:
        print(f"Error: {str(e)}")


# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])

@api_view(['POST'])
async def send(request):
    data = {
        'receiver_email': 'User954@example.com',
        'message_content': 'Hello, WebSocket!'
    }

    async def send_message():
        async with websockets.connect('ws://localhost:8000/ws/chat/send/') as websocket:
            await websocket.send(json.dumps(data))
            response = await websocket.recv()
            return Response({'response': response})

    response = await send_message()

    return Response({'response': response})
