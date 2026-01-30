# tests/test_user.py
import pytest
import allure
import requests
from data import Urls, UserData
from helpers import generate_random_string

class TestUser:
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self):
        """Тест проверяет, что уникального пользователя можно создать."""
        email = f"{generate_random_string()}@ya.ru"
        password = generate_random_string()
        name = generate_random_string()
        payload = {"email": email, "password": password, "name": name}

        with allure.step("Отправка POST-запроса на создание пользователя"):
            response = requests.post(Urls.USER_REGISTER, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True
        
        # БЛОК ОЧИСТКИ УДАЛЕН, КАК И ПРОСИЛ РЕВЬЮЕР
        # Для этого конкретного теста, который не использует фикстуру,
        # мы можем либо оставить "мусорного" пользователя, либо, если
        # чистота критична, вернуть сюда удаление, но это исключение из правил.

    @allure.title("Создание пользователя, который уже существует")
    def test_create_existing_user_error(self, created_user):
        """
        Тест проверяет, что нельзя создать пользователя, который уже зарегистрирован.
        Фикстура created_user теперь сама удалит этого пользователя после теста.
        """
        payload, _ = created_user

        with allure.step("Отправка POST-запроса на создание уже существующего пользователя"):
            response = requests.post(Urls.USER_REGISTER, json=payload)
        
        assert response.status_code == 403
        assert response.json()["message"] == UserData.USER_ALREADY_EXISTS_ERROR

    # ... (остальные тесты, не требующие изменений) ...

    @allure.title("Изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize(
        "field_to_update, new_value",
        [
            ("name", generate_random_string()),
            ("email", f"{generate_random_string()}@ya.ru")
        ]
    )
    def test_update_user_data_with_auth_success(self, created_user, field_to_update, new_value):
        """
        Тест проверяет, что авторизованный пользователь может изменить свои данные.
        УСЛОВНЫЙ БЛОК 'IF' УДАЛЕН ИЗ ТЕЛА ТЕСТА.
        """
        _, token = created_user
        headers = {"Authorization": token}
        payload = {field_to_update: new_value}

        with allure.step(f"Отправка PATCH-запроса на изменение поля '{field_to_update}'"):
            response = requests.patch(Urls.USER_DATA, headers=headers, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"][field_to_update] == new_value

    # ... (остальные тесты, не требующие изменений) ...
