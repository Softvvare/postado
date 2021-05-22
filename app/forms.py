from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.contrib.auth.models import User, Group, Permission
from django import forms
from django.db.models import fields
from app.validators import validate_email
from django.utils import timezone
import datetime as dt
from app.models import Comment, Post


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(
        max_length=255, required=True, validators=[validate_email])

    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2')

    def clean_first_name(self):
        cleaned_data = super(UserCreationForm, self).clean()
        first_name = cleaned_data.get("first_name")

        is_clean = self.blacklist_checker(first_name)

        if is_clean:
            return first_name
        else:
            raise forms.ValidationError('Invalid First Name')

    def clean_last_name(self):
        cleaned_data = super(UserCreationForm, self).clean()
        last_name = cleaned_data.get("last_name")

        is_clean = self.blacklist_checker(last_name)

        if is_clean:
            return last_name
        else:
            raise forms.ValidationError('Invalid Last Name')

    def blacklist_checker(self, string):

        blacklist = """,./?`~!@#$%^&*()|_-+="{[']}<\>"""
        is_clean = True

        for letter in string:
            if letter in blacklist:
                is_clean = False
                break
        else:
            is_clean = True

        return is_clean


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'photo']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
