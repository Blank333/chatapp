from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import ChatUserCreationForm, ChatUserChangeForm
from .models import ChatUser, Interest, UserInterest


class ChatUserAdmin(UserAdmin):
    add_form = ChatUserCreationForm
    form = ChatUserChangeForm
    model = ChatUser

    list_display = ('email', 'age', 'name', 'is_online', 'is_staff',)
    list_filter = ('email', 'age', 'name', 'is_online', 'is_staff', )

    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'age', 'is_online')}),
        ('Permissions', {'fields': ('is_staff', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'name', 'age', 'is_online', 'is_staff',
            )}
         ),
    )
    search_fields = ('email',)
    ordering = ('-created_at',)


class UserInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'interest', 'preference_score')
    list_filter = ('user', 'interest', 'preference_score')
    search_fields = ('user__name',)


class InterestAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('id', 'name')
    search_fields = ('name',)


admin.site.register(ChatUser, ChatUserAdmin)
admin.site.register(UserInterest, UserInterestAdmin)
admin.site.register(Interest, InterestAdmin)
