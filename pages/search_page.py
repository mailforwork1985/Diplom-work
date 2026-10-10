from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, Locator


class SearchPage(BasePage):
    # Используем name="text" — он статичен и точно есть в DOM
    SEARCH_INPUT: Locator = (By.NAME, "text")

    SUGGESTIONS: Locator = (By.ID, "suggest-container")

    def open_first_result(self) -> None:
        ("""Ждет исчезновения модального окна,
        затем кликает по первому результату.""")
        # 1. Ждем, пока исчезнет модальное окно (оверлей)
        # Это критически важно для Кинопоиска — там часто всплывают
        # баннеры/подсказки
        self.wait.until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, ".ReactModal__Overlay")
                )
        )
        # 2. Находим и кликаем по первой ссылке на фильм
        first_link = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a[href*='/film/'], a[href*='/movie/']")
                )
        )
        first_link.click()

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        super().__init__(driver, base_url)

    def type_query(self, query: str) -> None:
        input_field = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT),
            message="Не найдено поле поиска (name='text')"
        )
        input_field.clear()
        input_field.send_keys(query)

    def search(self, query: str) -> None:
        self.type_query(query)
        input_field = self.wait.until(
            EC.element_to_be_clickable(self.SEARCH_INPUT)
            )
        input_field.send_keys(Keys.ENTER)

    def expect_suggestions_visible(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self.SUGGESTIONS))
