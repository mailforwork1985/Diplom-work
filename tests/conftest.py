from typing import Iterator

import pytest
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

from api.client import ApiClient
from config.config import Config, load_config


@pytest.fixture(scope="session")
def config() -> Config:
    """Общая конфигурация на сессию."""
    return load_config()


@pytest.fixture(scope="session")
def api_client(config: Config) -> ApiClient:
    """API-клиент с валидным токеном."""
    return ApiClient(config.api_base_url, config.api_key)


@pytest.fixture(scope="session")
def start_of_inception_id(api_client: ApiClient) -> int:
    """API-005: ищет «Начало» и возвращает ID первого фильма."""
    response = api_client.get(
        "/v1.5/movie/search", params={"query": "Начало", "limit": 1}
        )
    assert response.status_code == 200, "Поиск «Начало» не выполнен"
    docs: list[dict] = response.json()["docs"]
    assert len(docs) >= 1, "Поиск не вернул результатов"
    return docs[0]["id"]


@pytest.fixture
def driver(config: Config) -> Iterator[WebDriver]:
    """Chrome для UI-тестов; закрывается после каждого теста."""
    options: Options = Options()
    options.add_argument("--window-size=1920,1080")
    driver: WebDriver = WebDriver(options=options)
    yield driver
    driver.quit()
