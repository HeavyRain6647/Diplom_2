# conftest.py
import pytest
import requests
from helpers import generate_random_string
from data import Urls

@pytest.fixture(scope="function")
def user_payload():
    """Генерирует данные для создания пользователя."""
    email = f"{generate_random_string()}@ya.ru"
    password = generate_random_string()
    name = generate_random_string()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    return payload

@pytest.fixture(scope="function")
def created_user(user_payload):
    """
    Создает пользователя с данными из user_payload,
    а после завершения теста удаляет его.
    """
    # Шаг 1: Создание пользователя (Setup)
    response = requests.post(Urls.USER_REGISTER, json=user_payload)
    token = response.json().get("accessToken")
    
    # Шаг 2: Передача данных в тест
    yield user_payload, token
    
    # Шаг 3: Очистка после теста (Teardown)
    if token:
        requests.delete(Urls.USER_DATA, headers={"Authorization": token})

# Фикстура ingredient_ids остается без изменений
@pytest.fixture(scope="session")
def ingredient_ids():
    response = requests.get(Urls.INGREDIENTS)
    return [item["_id"] for item in response.json()["data"]]
