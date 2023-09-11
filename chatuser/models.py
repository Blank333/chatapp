from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import ChatUserManager
from django.core.validators import MinValueValidator, MaxValueValidator

class ChatUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    age = models.IntegerField(validators=[MinValueValidator(14), MaxValueValidator(150)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'age']
    
    objects = ChatUserManager()
    
    def __str__(self):
        return self.name

class Interest(models.Model):
    name = models.CharField(max_length=128, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    
    
    def __str__(self):
        return self.name

class UserInterest(models.Model):
    user = models.ForeignKey(ChatUser, on_delete=models.CASCADE)
    interest = models.ForeignKey(Interest, on_delete=models.CASCADE)
    preference_score = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(100)]) 
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'interest')

    def __str__(self):
        return self.interest.name
    

class Message(models.Model):
    sender = models.ForeignKey(ChatUser, on_delete= models.PROTECT, related_name='sent_message')
    receiver = models.ForeignKey(ChatUser, on_delete= models.PROTECT, related_name='received_message')
    content = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)