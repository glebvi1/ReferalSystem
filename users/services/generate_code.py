import random
import string


def generate_invite_code() -> str:
    return "".join(random.choices(string.digits + string.ascii_lowercase + string.ascii_uppercase, k=6))


def generate_auth_code() -> str:
    return str(random.randint(1000, 9999))
