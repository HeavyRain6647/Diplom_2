import pytest
import requests
import random
import string
from urls import USER_REGISTER, USER_DATA

def generate_random_string(length=10):
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))

@pytest.fixture
def user_payload():
    """Генерирует случайные данные пользователя."""
    return {
        "email": f"{generate_random_string()}@yandex.ru",
        "password": "password123",
        "name": "Tester"
    }

@pytest.fixture
def created_user(user_payload):
    """Регистрирует пользователя и удаляет его после теста."""
    response = requests.post(USER_REGISTER, json=user_payload)
    token = response.json().get("accessToken")
    
    yield user_payload, token  # Передаем данные в тест
    
    # Удаление (Teardown): выполнится ПОСЛЕ теста
    if token:
        requests.delete(USER_DATA, headers={"Authorization": token})