from app.models import UserFollowing
from django.db import models
from django.contrib.auth.models import User
from app.models import UserFollowing, BaseModel


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    auth = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="room_author")
    receiver = models.ForeignKey(
        UserFollowing, on_delete=models.CASCADE, related_name="roomto_user")
    seen = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField(unique=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content
