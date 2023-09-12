from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from chatuser.models import ChatUser
from .serializers import StartChatSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


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


@api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def send(request):
    print("SENDING MESSAGE")
    return Response({'message': 'Chat sent successfully'}, status=status.HTTP_200_OK)
