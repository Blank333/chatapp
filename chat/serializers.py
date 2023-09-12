from rest_framework import serializers


class StartChatSerializer(serializers.Serializer):
    recipient_email = serializers.EmailField()
