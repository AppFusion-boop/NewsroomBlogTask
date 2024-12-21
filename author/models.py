from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils import timezone
from datetime import timedelta
from random import choices
import string


def generate_otp():
    return ''.join(choices(string.digits, k=6))


class Author(AbstractBaseUser):

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    otp = models.CharField(max_length=6, blank=True, null=True, default=generate_otp)
    otp_created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    def validate_otp(self, otp: str) -> bool:
        # time limit 5 minutes
        if self.otp_created_at < timezone.now() - timedelta(minutes=15):
            return False
        if self.otp == otp:
            self.is_active = True
            return True
