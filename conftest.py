# conftest.py
import pytest
import requests
from helpers import generate_random_string
from data import Urls

@pytest.fixture(scope="function")
def created_user():
    """
    Создает нового пользователя, возвращает его данные и токен.
    ПОСЛЕ ЗАВЕРШЕНИЯ ТЕСТА УДАЛЯЕТ СОЗДАННОГО ПОЛЬЗОВАТЕЛЯ.
    """
    email = f"{generate_random_string()}@ya.ru"
    password = generate_random_string()
    name = generate_random_string()

    payload = {
        "email": email,
        "password": password,
        "name": name
    }
    
    # Шаг 1: Создание пользователя (Setup)
    response = requests.post(Urls.USER_REGISTER, json=payload)
    token = response.json().get("accessToken")
    
    # Шаг 2: Передача данных в тест
    yield payload, token
    
    # Шаг 3: Очистка после теста (Teardown)
    if token:
        requests.delete(Urls.USER_DATA, headers={"Authorization": token})

@pytest.fixture(scope="session")
def ingredient_ids():
    """Получает и возвращает список реальных хешей ингредиентов."""
    response = requests.get(Urls.INGREDIENTS)
    return [item["_id"] for item in response.json()["data"]]
