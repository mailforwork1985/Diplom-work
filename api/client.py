from typing import Any
import pytest
import requests
from config import config
from typing import Iterator

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


@pytest.fixture
def driver(config: config) -> Iterator[WebDriver]:
    """Chrome для UI-тестов; закрывается после каждого теста."""
    options: Options = Options()
    # для прогонов без окна раскомментируйте:
    # options.add_argument("--headless=new")
    options.add_argument("--window-size=1920,1080")
    driver: WebDriver = WebDriver(options=options)
    yield driver
    driver.quit()


class ApiClient:
    """Обёртка над requests для kinopoisk.dev."""

    def __init__(self, base_url: str, api_key: str) -> None:
        self._base_url: str = base_url.rstrip("/")
        self._api_key: str = api_key

    def _headers(self, api_key: str | None) -> dict[str, str]:
        """Формирует заголовки; api_key позволяет подменить токен."""
        return {
            "accept": "application/json",
            "X-API-KEY": api_key or self._api_key,
        }

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        api_key: str | None = None,
    ) -> requests.Response:
        """GET-запрос к API."""
        return requests.get(
            f"{self._base_url}{path}",
            params=params,
            headers=self._headers(api_key),
            timeout=30,
        )

    def post(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        api_key: str | None = None,
    ) -> requests.Response:
        """POST-запрос к API (негативный кейс API-010)."""
        return requests.post(
            f"{self._base_url}{path}",
            params=params,
            headers=self._headers(api_key),
            timeout=30,
        )
