import requests
from urls import USER_REGISTER, USER_LOGIN

class TestUser:
    def test_create_unique_user_success(self, user_payload):
        # Используем payload, но регистрируем сами, чтобы проверить статус
        response = requests.post(USER_REGISTER, json=user_payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        # Очистка (для этого конкретного теста)
        token = response.json().get("accessToken")
        requests.delete("https://stellarburgers.education-services.ru/api/auth/user", headers={"Authorization": token})

    def test_create_existing_user_error(self, created_user):
        user_data, _ = created_user
        response = requests.post(USER_REGISTER, json=user_data)
        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"

    def test_create_user_missing_field_error(self):
        payload = {"email": "test@ya.ru", "name": "NoPass"} # Нет пароля
        response = requests.post(USER_REGISTER, json=payload)
        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"

    def test_login_success(self, created_user):
        user_data, _ = created_user
        payload = {"email": user_data["email"], "password": user_data["password"]}
        response = requests.post(USER_LOGIN, json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_login_wrong_credentials_error(self):
        payload = {"email": "wrong_1234567@ya.ru", "password": "wrong"}
        response = requests.post(USER_LOGIN, json=payload)
        assert response.status_code == 401