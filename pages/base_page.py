import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from config.settings import BASE_URL, EXPLICIT_WAIT


class BasePage:
    """
    Clase base para todas las páginas del framework.
    Encapsula las interacciones comunes con Selenium y Allure.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    # ── Navegación ──────────────────────────────────────────────────────────

    def open(self, path: str = "") -> None:
        self.driver.get(f"{BASE_URL}{path}")

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_title(self) -> str:
        return self.driver.title

    # ── Esperas y búsqueda ───────────────────────────────────────────────────

    def find(self, locator: tuple):
        return self.wait.until(
            EC.presence_of_element_located(locator),
            message=f"Elemento no encontrado: {locator}"
        )

    def find_all(self, locator: tuple) -> list:
        return self.wait.until(
            EC.presence_of_all_elements_located(locator),
            message=f"Elementos no encontrados: {locator}"
        )

    def find_clickable(self, locator: tuple):
        return self.wait.until(
            EC.element_to_be_clickable(locator),
            message=f"Elemento no clickeable: {locator}"
        )

    def find_visible(self, locator: tuple):
        return self.wait.until(
            EC.visibility_of_element_located(locator),
            message=f"Elemento no visible: {locator}"
        )

    def is_visible(self, locator: tuple) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except TimeoutException:
            return False

    def is_present(self, locator: tuple) -> bool:
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    # ── Acciones ─────────────────────────────────────────────────────────────

    def click(self, locator: tuple) -> None:
        self.find_clickable(locator).click()

    def type(self, locator: tuple, text: str) -> None:
        element = self.find(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.find(locator).text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        return self.find(locator).get_attribute(attribute)

    # ── JavaScript helpers ───────────────────────────────────────────────────

    def scroll_to(self, element) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)

    def scroll_and_click(self, locator: tuple) -> None:
        element = self.find_clickable(locator)
        self.scroll_to(element)
        element.click()

    def js_click(self, locator: tuple) -> None:
        element = self.find(locator)
        self.driver.execute_script("arguments[0].click();", element)

    def remove_ads(self) -> None:
        """Elimina banners de anuncios que bloquean interacciones en DemoQA."""
        self.driver.execute_script(
            "const el = document.querySelector('#fixedban'); if(el) el.remove();"
        )
        self.driver.execute_script(
            "const footer = document.querySelector('footer'); if(footer) footer.remove();"
        )

    # ── Allure ───────────────────────────────────────────────────────────────

    def take_screenshot(self, name: str = "screenshot") -> None:
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )
