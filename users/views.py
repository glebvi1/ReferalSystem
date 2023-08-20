from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users import (MESSAGE_BAD_FIELD_VERIFY, MESSAGE_BAD_VERIFY,
                   MESSAGE_SUCCESS_VERIFY, MESSAGE_SUCCESS_AUTH, MESSAGE_BAD_FIELD_INVITE,
                   MESSAGE_REUSE_INVITE, MESSAGE_NOT_FOUND_INVITE, MESSAGE_MYSELF_INVITE,
                   MESSAGE_NOT_VERIFIED)
from users.models import User
from users.serializers import UserSerializer
from users.services.user_service import assign_auth_code, verify_auth_code
from users.services.invite_code_service import get_user_by_invite_code


class LoginView(APIView):
    def post(self, request):
        assign_auth_code(request.user)
        content = {
            "auth_code": request.user.auth_code,
            "message": MESSAGE_SUCCESS_AUTH + str(request.user.id) + "/",
        }

        return Response(content, status=status.HTTP_200_OK)


@api_view(["POST"])
def verify_phone(request, pk):
    if "auth_code" not in request.data:
        return Response(MESSAGE_BAD_FIELD_VERIFY, status=status.HTTP_400_BAD_REQUEST)

    if not verify_auth_code(str(request.data["auth_code"]), pk):
        return Response(MESSAGE_BAD_VERIFY, status=status.HTTP_400_BAD_REQUEST)

    return Response(MESSAGE_SUCCESS_VERIFY, status=status.HTTP_200_OK)


class ProfileView(APIView):
    def get(self, request):
        if not request.user.is_verified():
            return Response(MESSAGE_NOT_VERIFIED, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UseInviteCode(APIView):
    def post(self, request):
        if not request.user.is_verified():
            return Response(MESSAGE_NOT_VERIFIED, status=status.HTTP_401_UNAUTHORIZED)

        if "invite_code" not in request.data:
            return Response(MESSAGE_BAD_FIELD_INVITE, status=status.HTTP_400_BAD_REQUEST)
        if request.data["invite_code"] == request.user.invite_code:
            return Response(MESSAGE_MYSELF_INVITE, status=status.HTTP_400_BAD_REQUEST)
        if (request.user.used_invite_code is not None) and (request.user.used_invite_code != request.data["invite_code"]):
            return Response(MESSAGE_REUSE_INVITE, status=status.HTTP_400_BAD_REQUEST)

        user = get_user_by_invite_code(request.user, request.data["invite_code"])

        if not user:
            return Response(MESSAGE_NOT_FOUND_INVITE, status=status.HTTP_400_BAD_REQUEST)

        return Response(UserSerializer(user).data)


class GetListInviters(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(used_invite_code=self.request.user.invite_code)
