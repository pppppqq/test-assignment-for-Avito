import pytest
import requests


@pytest.mark.positive
def test_create_item_returns_success_status(base_url, seller_id, random_item_name):
    """Проверяет, что создание элемента возвращает успешный статус.

    Шаги теста:
    1. Формируется payload с обязательными полями: sellerId, name, price, statistics.
    2. Выполняется POST-запрос к /api/1/item.
    3. Проверяется, что код ответа 200.
    """
    payload = {
        "sellerId": seller_id,
        "name": random_item_name,
        "price": 500,
        "statistics": {"likes": 100, "viewCount": 100, "contacts": 100}
    }
    response = requests.post(f"{base_url}/api/1/item", json=payload)

    assert response.status_code == 200


@pytest.mark.xfail(reason="Баг: API должен возвращать структуру объекта вместо строкового сообщения.")
def test_create_item_returns_proper_structure(base_url, seller_id, random_item_name):
    """Проверяет корректность структуры ответа при создании элемента.

    Шаги теста:
    1. Формируется payload с обязательными полями.
    2. Выполняется POST-запрос к /api/1/item.
    3. Проверяется, что код ответа 200.
    4. Проверяется структура возвращаемого объекта:
       - наличие полей 'id', 'sellerId', 'name', 'createdAt';
       - совпадение sellerId и name с отправленными данными.
    """
    payload = {
        "sellerId": seller_id,
        "name": random_item_name,
        "price": 500,
        "statistics": {"likes": 100, "viewCount": 100, "contacts": 100}
    }
    response = requests.post(f"{base_url}/api/1/item", json=payload)

    assert response.status_code == 200
    data = response.json()

    # Эти assertions будут падать пока баг не починят
    assert "id" in data
    assert "sellerId" in data
    assert data["sellerId"] == seller_id
    assert data["name"] == random_item_name
    assert "createdAt" in data


@pytest.mark.negative
@pytest.mark.parametrize("payload", [
    {"name": "test", "price": 500},                  # без sellerId
    {"sellerId": 123, "price": 500},                 # без name
    {"sellerId": 123, "name": "test"},              # без price
])
def test_create_item_missing_fields(base_url, payload):
    """Проверяет создание элемента с отсутствующими обязательными полями.

    Шаги теста:
    1. Параметризованные payload без одного из обязательных полей.
    2. Выполняется POST-запрос к /api/1/item.
    3. Проверяется, что код ответа 400.
    """
    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 400


@pytest.mark.negative
def test_create_item_invalid_data(base_url):
    """Проверяет создание элемента с некорректными данными.

    Шаги теста:
    1. Формируется payload с неверным sellerID (строка вместо числа).
    2. Выполняется POST-запрос к /api/1/item.
    3. Проверяется, что код ответа 400.
    """
    payload = {
        "sellerId": "invalid_id",
        "name": "test",
        "price": 1000,
        "statistics": {"likes": 5, "viewCount": 150, "contacts": 10}
    }
    response = requests.post(f"{base_url}/api/1/item", json=payload)
    assert response.status_code == 400
