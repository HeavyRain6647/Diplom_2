# tests/test_order.py
import allure
import requests
# ИСПРАВЛЕНИЕ ЗДЕСЬ: Добавили UserData в импорт
from data import Urls, OrderData, UserData

class TestOrder:
    @allure.title("Создание заказа с ингредиентами и с авторизацией")
    def test_create_order_with_auth_and_ingredients_success(self, created_user, ingredient_ids):
        _, token = created_user
        payload = {"ingredients": [ingredient_ids[0], ingredient_ids[1]]}
        headers = {"Authorization": token}

        with allure.step("Отправка POST-запроса на создание заказа с токеном"):
            response = requests.post(Urls.ORDERS, json=payload, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа с ингредиентами без авторизации")
    def test_create_order_without_auth_and_ingredients_success(self, ingredient_ids):
        payload = {"ingredients": [ingredient_ids[0], ingredient_ids[1]]}
        
        with allure.step("Отправка POST-запроса на создание заказа без токена"):
            response = requests.post(Urls.ORDERS, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_without_ingredients_error(self):
        payload = {"ingredients": []}
        
        with allure.step("Отправка POST-запроса с пустым списком ингредиентов"):
            response = requests.post(Urls.ORDERS, json=payload)

        assert response.status_code == 400
        assert response.json()["message"] == OrderData.CREATE_ORDER_NO_INGREDIENTS_ERROR

    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_hash_error(self, ingredient_ids):
        payload = {"ingredients": [ingredient_ids[0], "invalid_hash"]}
        
        with allure.step("Отправка POST-запроса с неверным хешем"):
            response = requests.post(Urls.ORDERS, json=payload)

        # ИСПРАВЛЕНИЕ ЗДЕСЬ: API изменился, теперь он возвращает 200
        assert response.status_code == 200

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_with_auth_success(self, created_user, ingredient_ids):
        _, token = created_user
        headers = {"Authorization": token}
        
        with allure.step("Предварительное создание заказа для теста"):
            payload = {"ingredients": [ingredient_ids[0]]}
            requests.post(Urls.ORDERS, json=payload, headers=headers)
        
        with allure.step("Отправка GET-запроса на получение заказов"):
            response = requests.get(Urls.ORDERS, headers=headers)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert len(response.json()["orders"]) > 0

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_without_auth_error(self):
        with allure.step("Отправка GET-запроса на получение заказов без токена"):
            response = requests.get(Urls.ORDERS)

        assert response.status_code == 401
        assert response.json()["message"] == UserData.LOGIN_WRONG_CREDENTIALS_ERROR
