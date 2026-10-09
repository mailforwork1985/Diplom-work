import re
from typing import Pattern

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, Locator


class MoviePage(BasePage):
    """Карточка фильма: название, рейтинг, описание."""

    TITLE: Locator = (By.CSS_SELECTOR, "h1")
    RATING: Locator = (By.CSS_SELECTOR, 
                       ".film-rating-value, [data-test-id*='ratingNumber']")
    RATING_PATTERN: Pattern[str] = re.compile(r"^\d\.\d$")

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        super().__init__(driver, base_url)

    def expect_title_visible(self) -> None:
        """Заголовок карточки отображается."""
        self.wait.until(EC.visibility_of_element_located(self.TITLE))

    def expect_description_visible(self) -> None:
        """Блок описания фильма отображается."""
        self.wait.until(EC.visibility_of_any_elements_located(
            (By.CSS_SELECTOR, "p"))
            )

    def get_rating_text(self) -> str:
        """Возвращает текст рейтинга, дождавшись его появления."""
        rating = self.wait.until(EC.visibility_of_element_located(self.RATING))
        return rating.text.strip()
