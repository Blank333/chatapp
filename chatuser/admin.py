from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ChatUserCreationForm, ChatUserChangeForm
from .models import ChatUser, Interest, UserInterest


class ChatUserAdmin(UserAdmin):
    add_form = ChatUserCreationForm
    form = ChatUserChangeForm
    model = ChatUser

    list_display = ('email', 'age', 'name', 'is_staff',)
    list_filter = ('email', 'age', 'name', 'is_staff', )

    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'age')}),
        ('Permissions', {'fields': ('is_staff', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'name', 'age', 'is_staff',
            )}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'interest', 'preference_score')
    list_filter =  ('user', 'interest', 'preference_score')


admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(UserInterest, UserInterestAdmin)
admin.site.register(Interest)