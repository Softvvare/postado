from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(f"{value} is taken.", params={'value': value})