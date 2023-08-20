from django.contrib.auth import authenticate, get_user_model
from rest_framework import authentication

from users.services.user_service import check_phone_number, refactor_phone_number

User = get_user_model()


class PhoneAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        phone_number = request.data.get("phone_number")
        if not phone_number or not check_phone_number(phone_number):
            return None

        phone_number = refactor_phone_number(phone_number)
        user = authenticate(phone_number=phone_number)

        return user, None
