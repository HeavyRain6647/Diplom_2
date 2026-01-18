import requests
from urls import ORDERS, INGREDIENTS

class TestOrder:
    @pytest.fixture
    def ingredient_ids(self):
        """Получает список реальных хешей ингредиентов."""
        response = requests.get(INGREDIENTS)
        return [item["_id"] for item in response.json()["data"]]

    def test_create_order_with_auth(self, created_user, ingredient_ids):
        _, token = created_user
        payload = {"ingredients": [ingredient_ids[0], ingredient_ids[1]]}
        headers = {"Authorization": token}
        response = requests.post(ORDERS, json=payload, headers=headers)
        assert response.status_code == 200
        assert response.json()["success"] is True

    def test_create_order_without_auth(self, ingredient_ids):
        payload = {"ingredients": [ingredient_ids[0]]}
        response = requests.post(ORDERS, json=payload)
        assert response.status_code == 200 # API позволяет это
        assert response.json()["success"] is True

    def test_create_order_with_ingredients(self, ingredient_ids):
        payload = {"ingredients": ingredient_ids[:2]}
        response = requests.post(ORDERS, json=payload)
        assert response.status_code == 200
        assert "order" in response.json()

    def test_create_order_no_ingredients(self):
        payload = {"ingredients": []}
        response = requests.post(ORDERS, json=payload)
        assert response.status_code == 400
        assert response.json()["message"] == "Ingredient ids must be provided"

    def test_create_order_invalid_hash(self):
        payload = {"ingredients": ["invalid_hash_123"]}
        response = requests.post(ORDERS, json=payload)
        assert response.status_code == 500