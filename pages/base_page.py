from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]


class BasePage:
    """Базовый Page Object: навигация и ожидания."""

    DEFAULT_TIMEOUT: int = 10

    def __init__(self, driver: WebDriver, base_url: str) -> None:
        self.driver: WebDriver = driver
        self.base_url: str = base_url.rstrip("/")
        self.wait: WebDriverWait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)

    def open(self, path: str = "") -> None:
        """Открывает страницу."""
        self.driver.get(f"{self.base_url}{path}")

    def find(self, locator: Locator) -> object:
        """Ищет элемент с явным ожиданием появления."""
        return self.wait.until(
            lambda d: d.find_element(By.CSS_SELECTOR, locator[1])
            if locator[0] == "css" else d.find_element(*locator)
        )
