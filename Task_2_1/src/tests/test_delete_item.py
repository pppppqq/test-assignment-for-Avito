import pytest
import requests


@pytest.mark.positive
def test_delete_existing_item(base_url, create_test_item_for_delete):
    """Проверяет удаление существующего элемента по его ID.

    Шаги теста:
    1. Получается ID тестового элемента для удаления.
    2. Выполняется DELETE-запрос к /api/2/item/{item_id}.
    3. Проверяется, что код ответа 200, что указывает на успешное удаление.
    """
    item_id = create_test_item_for_delete["id"]
    response = requests.delete(f"{base_url}/api/2/item/{item_id}")
    assert response.status_code == 200


@pytest.mark.negative
def test_delete_nonexistent_item(base_url, random_uuid):
    """Проверяет удаление несуществующего элемента.

    Шаги теста:
    1. Выполняется DELETE-запрос к /api/2/item/{random_uuid}.
    2. Проверяется, что код ответа 404.
    3. Печатается тело ответа для отладки.
    """
    response = requests.delete(f"{base_url}/api/2/item/{random_uuid}")
    print(response.json())
    assert response.status_code == 404


@pytest.mark.negative
def test_delete_invalid_id(base_url):
    """Проверяет поведение API при попытке удалить элемент с некорректным ID.

    Шаги теста:
    1. Выполняется DELETE-запрос к /api/2/item/invalid_id.
    2. Проверяется, что код ответа 400.
    """
    response = requests.delete(f"{base_url}/api/2/item/invalid_id")
    assert response.status_code == 400
