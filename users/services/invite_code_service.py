from users.models import User
from typing import Optional


def get_user_by_invite_code(current_user: User, invite_code: str) -> Optional[User]:
    """Функция возвращает пользователя по код приглашению, если такой есть, None иначе"""
    user = User.objects.filter(invite_code=invite_code)
    if user.exists():
        current_user.used_invite_code = invite_code
        current_user.save()
        return user.first()

    return None
