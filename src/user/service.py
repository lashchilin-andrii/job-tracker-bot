from src.user.schema import User


def user_to_str(user: User):
    username = user.user_name or "NoUsername"
    first_name = user.user_first_name or ""
    last_name = user.user_last_name or ""
    language = user.user_language

    return (
        f"@{username}\nName: {first_name} {last_name}".strip()
        + f"\nLanguage: {language}"
    )
