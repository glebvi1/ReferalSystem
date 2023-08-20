from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)
    auth_code = models.CharField(max_length=4, null=True, default=None)

    invite_code = models.CharField(max_length=6, unique=True)
    used_invite_code = models.CharField(max_length=6, null=True, default=None)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    def is_verified(self):
        return self.auth_code is None

    def __str__(self):
        return f"Phone: {self.phone_number} Auth: {self.auth_code} Invite: {self.invite_code}"
