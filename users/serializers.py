from rest_framework import serializers, fields

from users.models import User


class UserSerializer(serializers.ModelSerializer):

    invitor = fields.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "phone_number", "invite_code", "used_invite_code", "invitor")

    def get_invitor(self, obj):
        user = User.objects.filter(invite_code=obj.used_invite_code)
        return user.first().phone_number if user.exists() else None
