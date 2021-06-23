from .models import ChatRoom, Messages
from django import forms


class CreateMessagesForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['content']


class CreateRoomForm(forms.ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['receiver']
