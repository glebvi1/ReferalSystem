from django.contrib.auth import get_user_model

from users.services.generate_code import (generate_auth_code,
                                          generate_invite_code)

User = get_user_model()


class PhoneAuthBackend:
    def authenticate(self, request, phone_number=None):
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            user = User.objects.create(phone_number=phone_number,
                                       auth_code=generate_auth_code(),
                                       invite_code=generate_invite_code())
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None
