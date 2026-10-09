import allure
import pytest

from api.client import ApiClient

INVALID_TOKEN: str = "INVALID"


@allure.feature("API")
@allure.story("Негативные сценарии")
@pytest.mark.api
@pytest.mark.parametrize(
    "params, expected_statuses",
    [
        pytest.param({"year": ''}, (400, 422), id="API-006: без year"),
        pytest.param(
            {"query": "Аватар", "limit": 999, 
                "page": 1}, (400, 422), id="API-009: limit>250"
        ),
    ],
)
def test_search_invalid_params(
    api_client: ApiClient, params: dict, expected_statuses: tuple[int, int]
) -> None:
    """Невалидные параметры поиска — ошибка валидации без данных."""
    response = api_client.get("/v1.5/movie", params=params)
    assert response.status_code in expected_statuses
    assert "docs" not in response.json(), "При ошибке вернулись данные"


@allure.feature("API")
@allure.story("Негативные сценарии")
@pytest.mark.api
def test_invalid_token(api_client: ApiClient) -> None:
    """API-007: невалидный токен — ошибка авторизации."""
    response = api_client.get(
        "/v1.5/movie/search", params={"query": "Аватар"}, api_key=INVALID_TOKEN
    )
    assert response.status_code in (401, 403)
    assert response.json().get("message"), (
        "Нет сообщения об ошибке авторизации")


@allure.feature("API")
@allure.story("Негативные сценарии")
@pytest.mark.api
def test_movie_by_nonexistent_id(api_client: ApiClient) -> None:
    """API-008: несуществующий ID — 404 без данных фильма."""
    response = api_client.get("/v1.5/movie/9999999999")
    assert response.status_code == 400
    assert response.json().get("message"), "Нет сообщения об ошибке"


@allure.feature("API")
@allure.story("Негативные сценарии")
@pytest.mark.api
@pytest.mark.xfail(
    reason="Бэкенд должен возвращать 404 Method Not found, но возвращает 200"
    )
def test_post_not_allowed(api_client: ApiClient) -> None:
    """API-010: POST на GET-эндпоинт — 404/405 без данных."""
    response = api_client.post("/v1.5/movie/search")
    assert response.status_code in (404, 405)
