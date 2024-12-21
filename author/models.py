from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta
from random import choices
import string


def generate_otp():
    return ''.join(choices(string.digits, k=6))


class Author(AbstractUser):

    profile_picture = models.ImageField(upload_to='author_images/', blank=True, null=True)

    otp = models.CharField(max_length=6, blank=True, null=True, default=generate_otp)
    otp_created_at = models.DateTimeField(auto_now_add=True)

    def validate_otp(self, otp: str) -> bool:
        # time limit 5 minutes
        if self.otp_created_at < timezone.now() - timedelta(minutes=15):
            return False
        if self.otp == otp:
            self.is_active = True
            return True
