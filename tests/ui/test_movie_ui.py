import allure
import pytest
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import Config
from pages.movie_page import MoviePage
from pages.search_page import SearchPage


@pytest.fixture
def movie_page(driver: WebDriver, config: Config) -> MoviePage:
    """Карточка фильма «Начало», открытая из поиска — на каждый тест своя."""
    sp: SearchPage = SearchPage(driver, config.web_url)
    sp.open("/")
    sp.search("Начало")
    sp.open_first_result()
    return MoviePage(driver, config.web_url)


@allure.feature("UI")
@allure.story("Карточка фильма")
@pytest.mark.ui
def test_movie_card_opens(movie_page: MoviePage) -> None:
    """UI-002: карточка содержит название и описание."""
    movie_page.expect_title_visible()
    movie_page.expect_description_visible()


@allure.feature("UI")
@allure.story("Карточка фильма")
@pytest.mark.ui
def test_movie_rating_format(movie_page: MoviePage) -> None:
    """UI-004: рейтинг в формате X.X и не пустой."""
    rating: str = movie_page.get_rating_text()
    assert MoviePage.RATING_PATTERN.match(rating), f"Рейтинг «{rating}» не в формате X.X"
