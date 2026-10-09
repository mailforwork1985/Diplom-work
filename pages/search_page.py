from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage, Locator


class SearchPage(BasePage):
    """Поисковая строка, подсказки и результаты поиска."""

    SEARCH_INPUT: Locator = (By.CSS_SELECTOR, "input[class='styles_inputActive__4zFjs']")
    SUGGESTIONS: Locator = (
        By.CSS_SELECTOR, "ul[role='listbox'], [data-test-id*='suggest']"
        )

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        super().__init__(driver, base_url)

    def type_query(self, query: str) -> None:
        """Вводит запрос без нажатия Enter (для подсказок, UI-003)."""
        input_field = self.wait.until(
            EC.presence_of_element_located(self.SEARCH_INPUT)
        )
        input_field.clear()
        input_field.send_keys(query)

    def search(self, query: str) -> None:
        """Вводит запрос и отправляет его Enter'ом."""
        self.type_query(query)
        input_field = self.driver.find_element(*self.SEARCH_INPUT)
        input_field.send_keys(Keys.ENTER)

    def expect_suggestions_visible(self) -> None:
        """Подсказки появились под полем ввода."""
        self.wait.until(EC.visibility_of_element_located(self.SUGGESTIONS))

    def open_first_result(self) -> None:
        """Открывает первую ссылку на фильм из результатов поиска."""
        link = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='/film/']"))
        )
        link.click()
