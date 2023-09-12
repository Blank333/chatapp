from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import ChatUser, Interest, UserInterest

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
class InterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('id', 'name')

class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = ('interest', 'preference_score')

class ChatUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    interests = serializers.ListField(write_only=True, required=True)

    class Meta:
        model = ChatUser
        fields = ['id', 'email', 'name', 'age', 'password', 'interests']
    
    def create(self, validated_data):
        interests_data = validated_data.pop('interests')
        user = ChatUser.objects.create_user(**validated_data)

        for interest_data in interests_data:
            if interest_data['preference_score'] == 0: continue

            interest_name = interest_data.get('name')
            preference_score = interest_data.get('preference_score', 0)


            interest = Interest.objects.get(name=interest_name)
            UserInterest.objects.create(user=user, interest=interest, preference_score=preference_score)
        return user
    
    def validate_interests(self, value):
        if len(value) < 3 or len(value) > 6:
            raise serializers.ValidationError("You must select between 3 and 6 interests.")
        
        interest_names = [item['name'] for item in value]
        existing_interests = Interest.objects.filter(name__in=interest_names)
        
        if len(existing_interests) != len(value):
            raise serializers.ValidationError("One or more selected interests do not exist.")
        
        return value

    
class ChatUserCreationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = ChatUser
        fields = ('email', 'age', 'name')

    def create(self, validated_data):
        user = ChatUser.objects.create_user(**validated_data)
        return user

class ChatUserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUser
        fields = ('email', 'age', 'name')
