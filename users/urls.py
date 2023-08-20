from django.urls import path

from users.views import LoginView, ProfileView, verify_phone, UseInviteCode, GetListInviters

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("verify/<int:pk>/", verify_phone, name="verify"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("use_invite_code/", UseInviteCode.as_view(), name="use_invite_code"),
    path("list_inviters/", GetListInviters.as_view(), name="list_inviters"),
]
