import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from config.config import Config
from pages.search_page import SearchPage


@pytest.fixture
def search_page(driver: WebDriver, config: Config) -> SearchPage:
    """Открытая главная страница — свой браузер на каждый тест."""
    sp: SearchPage = SearchPage(driver, config.web_url)
    sp.open("/")
    return sp


def _wait_text_visible(driver: WebDriver, text: str) -> None:
    """Явное ожидание появления текста на странице."""
    SearchPage(driver, "").wait.until(
        EC.presence_of_element_located(
            (By.XPATH, f"//*[contains(normalize-space(.), '{text}')]")
        )
    )


@allure.feature("UI")
@allure.story("Поиск")
@pytest.mark.ui
def test_search_film_by_name(driver: WebDriver, search_page: SearchPage) -> None:
    """UI-001: поиск «Аватар» открывает страницу с результатами."""
    search_page.search("Аватар")
    _wait_text_visible(driver, "Аватар")


@allure.feature("UI")
@allure.story("Поиск")
@pytest.mark.ui
def test_search_suggestions_appear(search_page: SearchPage) -> None:
    """UI-003: при вводе без Enter появляются подсказки."""
    search_page.type_query("Нач")
    search_page.expect_suggestions_visible()


@allure.feature("UI")
@allure.story("Поиск")
@pytest.mark.ui
def test_search_series_by_name(driver: WebDriver, search_page: SearchPage) -> None:
    """UI-005: «Во все тяжкие» находится в результатах."""
    search_page.search("Во все тяжкие")
    _wait_text_visible(driver, "Во все тяжкие")
