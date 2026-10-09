import allure
import pytest

from api.client import ApiClient


@allure.feature("API")
@allure.story("Карточка фильма")
@pytest.mark.api
def test_get_movie_by_id(api_client: ApiClient) -> None:
    """API-002: фильм по ID 666 существует и содержит name и rating."""
    response = api_client.get("/v1.4/movie/666")
    assert response.status_code == 200
    body: dict = response.json()
    assert body.get("id") == 666, "ID в ответе не совпадает с запрошенным"
    assert body.get("name"), "Поле name отсутствует или пустое"
    assert body.get("rating") is not None, "Поле rating отсутствует"


@allure.feature("API")
@allure.story("Карточка фильма")
@pytest.mark.api
def test_get_random_movie(api_client: ApiClient) -> None:
    """API-004: случайный фильм содержит id и name."""
    response = api_client.get("/v1.4/movie/random")
    assert response.status_code == 200
    body: dict = response.json()
    assert "id" in body, "Нет поля id"
    assert "names" in body, "Нет поля name"
