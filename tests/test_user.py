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
        
        # Очистка
        token = response.json().get("accessToken")
        if token:
            requests.delete(Urls.USER_DATA, headers={"Authorization": token})

    @allure.title("Создание пользователя, который уже существует")
    def test_create_existing_user_error(self, created_user):
        """Тест проверяет, что нельзя создать пользователя, который уже зарегистрирован."""
        payload, _ = created_user

        with allure.step("Отправка POST-запроса на создание уже существующего пользователя"):
            response = requests.post(Urls.USER_REGISTER, json=payload)
        
        assert response.status_code == 403
        assert response.json()["message"] == UserData.USER_ALREADY_EXISTS_ERROR

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field_error(self, missing_field):
        """Тест проверяет, что нельзя создать пользователя, если не заполнено одно из обязательных полей."""
        payload = {
            "email": f"{generate_random_string()}@ya.ru",
            "password": generate_random_string(),
            "name": generate_random_string()
        }
        del payload[missing_field]

        with allure.step(f"Отправка POST-запроса без поля '{missing_field}'"):
            response = requests.post(Urls.USER_REGISTER, json=payload)

        assert response.status_code == 403
        assert response.json()["message"] == UserData.CREATE_USER_MISSING_FIELD_ERROR
    
    @allure.title("Успешный логин пользователя")
    def test_login_user_success(self, created_user):
        """Тест проверяет успешную авторизацию пользователя."""
        payload, _ = created_user

        with allure.step("Отправка POST-запроса для логина"):
            response = requests.post(Urls.USER_LOGIN, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Логин с неверным логином и паролем")
    @pytest.mark.parametrize("field", ["email", "password"])
    def test_login_wrong_credentials_error(self, created_user, field):
        """Тест проверяет, что с неверным логином или паролем залогиниться нельзя."""
        payload, _ = created_user
        payload[field] = "wrong_credentials"
        
        with allure.step(f"Отправка POST-запроса с неверным полем '{field}'"):
            response = requests.post(Urls.USER_LOGIN, json=payload)

        assert response.status_code == 401
        assert response.json()["message"] == UserData.LOGIN_WRONG_CREDENTIALS_ERROR

    @allure.title("Изменение данных пользователя с авторизацией")
    @pytest.mark.parametrize("field_to_update", ["email", "name"])
    def test_update_user_data_with_auth_success(self, created_user, field_to_update):
        """Тест проверяет, что авторизованный пользователь может изменить свои данные (email и имя)."""
        _, token = created_user
        headers = {"Authorization": token}
        new_value = generate_random_string()
        
        # Если обновляем email, он должен быть в корректном формате
        if field_to_update == "email":
            new_value += "@ya.ru"
            
        payload = {field_to_update: new_value}

        with allure.step(f"Отправка PATCH-запроса на изменение поля '{field_to_update}'"):
            response = requests.patch(Urls.USER_DATA, headers=headers, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert response.json()["user"][field_to_update] == new_value

    @allure.title("Изменение данных пользователя без авторизации")
    def test_update_user_data_without_auth_error(self):
        """Тест проверяет, что неавторизованный пользователь не может изменить свои данные."""
        payload = {"name": "new_name"}
        
        with allure.step("Отправка PATCH-запроса без токена авторизации"):
            response = requests.patch(Urls.USER_DATA, json=payload)

        assert response.status_code == 401
        assert response.json()["message"] == UserData.UPDATE_UNAUTHORIZED_ERROR
