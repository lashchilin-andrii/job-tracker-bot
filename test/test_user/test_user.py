from src.user.schema import User
from src.user.service import user_to_str


def test_profile():
    user = User(
        user_id="123e4567-e89b-12d3-a456-426614174000",
        user_name="testuser",
        user_first_name="John",
        user_last_name="Doe",
        user_language="en",
    )

    result = user_to_str(user)

    expected = "@testuser\nName: John Doe\nLanguage: en"
    assert result == expected


def test_profile_missing_optional_fields():
    user = User(
        user_id="123e4567-e89b-12d3-a456-426614174001",
        user_name=None,
        user_first_name="Jane",
        user_last_name=None,
        user_language="en",
    )

    result = user_to_str(user)

    expected = "@NoUsername\nName: Jane\nLanguage: en"
    assert result == expected
