from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import ChatUser


class ChatUserCreationForm(UserCreationForm):

    class Meta:
        model = ChatUser
        fields = ('email', 'age', 'name')


class ChatUserChangeForm(UserChangeForm):

    class Meta:
        model = ChatUser
        fields = ('email', 'age', 'name')