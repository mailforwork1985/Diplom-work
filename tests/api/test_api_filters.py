import allure
import pytest

from api.client import ApiClient


@allure.feature("API")
@allure.story("Фильтрация")
@pytest.mark.api
def test_filter_by_year_and_genre(api_client: ApiClient) -> None:
    """API-003: фильтры year и genres.name сужают выдачу по диапазону."""
    response = api_client.get(
        "/v1.4/movie",
        params={"year": "2020-2024", "genres.name": "драма", "limit": 10},
    )
    assert response.status_code == 200
    docs: list[dict] = response.json()["docs"]
    for movie in docs:
        year: int = movie["year"]
        assert 2020 <= year <= 2024, f"Год {year} вне диапазона 2020–2024"
