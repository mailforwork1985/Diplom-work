import allure
import pytest

from api.client import ApiClient

SEARCH: str = "/v1.4/movie/search"


@allure.feature("API")
@allure.story("Поиск фильма")
@pytest.mark.api
@pytest.mark.parametrize("query", ["Аватар", "Во все тяжкие"])
def test_search_by_name(api_client: ApiClient, query: str) -> None:
    """API-001: поиск по названию возвращает список не длиннее limit."""
    response = api_client.get(
        SEARCH, params={"query": query, "page": 1, "limit": 10}
        )
    assert response.status_code == 200
    docs: list[dict] = response.json()["docs"]
    assert isinstance(docs, list), "docs — не массив"
    assert len(docs) <= 10, f"Получено {len(docs)} результатов при limit=10"


@allure.feature("API")
@allure.story("Поиск фильма")
@pytest.mark.api
def test_search_saves_movie_id(
    api_client: ApiClient, start_of_inception_id: int
) -> None:
    """API-005: поиск «Начало» и сохранение ID первого фильма."""
    assert isinstance(start_of_inception_id, int), "ID фильма не число"
