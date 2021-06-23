from django.db import models
from django.contrib.auth.models import User


class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True, blank=False)
    users = models.ManyToManyField(
        User, help_text="users who are connected to the chat")

    def __str__(self):
        return self.name

    def connect_user(self, user):
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True

        return is_user_added

    def disconnect_user(self, user):
        is_user_removed = False
        if user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True

        return is_user_removed

    @property
    def group_name(self):
        return f"ChatRoom-{self.id}"


class ChatMessagesManager(models.Model):

    def by_room(self, room):
        qs = Messages.objects.filter(room=room).order_by("-created_date")
        return qs


class Messages(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content = models.TextField(unique=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = ChatMessagesManager()

    def __str__(self):
        return self.content
