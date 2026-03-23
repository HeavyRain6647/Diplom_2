# tests/test_user.py
import pytest
import allure
import requests
from data import Urls, UserData

# helpers больше не нужен в этом файле, так как генерация вынесена в conftest

class TestUser:
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, user_payload): # Используем новую фикстуру
        """
        Тест проверяет, что уникального пользователя можно создать.
        После теста пользователь удаляется.
        """
        with allure.step("Отправка POST-запроса на создание пользователя"):
            response = requests.post(Urls.USER_REGISTER, json=user_payload)

        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        assert response.json()["success"] is True, "Поле 'success' не равно true"

        # --- ИСПРАВЛЕНИЕ: Добавляем шаг очистки, как просил ревьюер ---
        with allure.step("Очистка: удаление созданного пользователя"):
            token = response.json().get("accessToken")
            if token:
                delete_response = requests.delete(Urls.USER_DATA, headers={"Authorization": token})
                assert delete_response.status_code == 202, "Не удалось удалить пользователя после теста"

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

    # ... (все остальные тесты остаются без изменений)
