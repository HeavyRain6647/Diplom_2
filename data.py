# data.py

class Urls:
    """Класс для хранения URL-адресов API."""
    BASE_URL = "https://stellarburgers.education-services.ru/api"
    INGREDIENTS = f"{BASE_URL}/ingredients"
    ORDERS = f"{BASE_URL}/orders"
    USER_REGISTER = f"{BASE_URL}/auth/register"
    USER_LOGIN = f"{BASE_URL}/auth/login"
    USER_DATA = f"{BASE_URL}/auth/user"

class UserData:
    """Класс для хранения данных, связанных с пользователем."""
    CREATE_USER_MISSING_FIELD_ERROR = "Email, password and name are required fields"
    USER_ALREADY_EXISTS_ERROR = "User with such email already exists"
    LOGIN_WRONG_CREDENTIALS_ERROR = "You should be authorised" # У API именно такой ответ
    UPDATE_UNAUTHORIZED_ERROR = "You should be authorised"

class OrderData:
    """Класс для хранения данных, связанных с заказами."""
    CREATE_ORDER_NO_INGREDIENTS_ERROR = "Ingredient ids must be provided"
    CREATE_ORDER_INVALID_HASH_ERROR = "One or more ids provided are incorrect"
