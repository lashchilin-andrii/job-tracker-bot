import pytest
from faker import Faker

from src.user.schema import User
from src.user.service import render_profile


@pytest.fixture
def fake():
    return Faker()


def test_profile(fake):
    user = User(
        user_id=fake.uuid4(),
        user_name=fake.user_name(),
        user_first_name=fake.first_name(),
        user_last_name=fake.last_name(),
        user_language=fake.language_code(),
    )

    result = render_profile(user)

    expected = (
        f"@{user.user_name}\n\n"
        f"🧑 Name: {user.user_first_name} {user.user_last_name}\n\n"
        f"🌐 Language: {user.user_language}"
    )

    assert result == expected


def test_profile_missing_optional_fields(fake):
    user = User(
        user_id=fake.uuid4(),
        user_name=None,
        user_first_name=fake.first_name(),
        user_last_name=None,
        user_language=fake.language_code(),
    )

    result = render_profile(user)

    print(result)

    expected = (
        f"@NoUsername\n\n"
        f"🧑 Name: {user.user_first_name}\n\n"
        f"🌐 Language: {user.user_language}"
    )

    assert result == expected
