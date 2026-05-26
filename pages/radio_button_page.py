import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RadioButtonPage(BasePage):
    PATH = "/radio-button"

    # ── Locators ─────────────────────────────────────────────────────────────
    YES_RADIO = (By.CSS_SELECTOR, "label[for='yesRadio']")
    IMPRESSIVE_RADIO = (By.CSS_SELECTOR, "label[for='impressiveRadio']")
    NO_RADIO = (By.CSS_SELECTOR, "label[for='noRadio']")
    NO_RADIO_INPUT = (By.ID, "noRadio")

    OUTPUT_TEXT = (By.CSS_SELECTOR, ".mt-3 span.text-success")

    # ── Actions ───────────────────────────────────────────────────────────────

    @allure.step("Abrir página Radio Button")
    def open(self) -> "RadioButtonPage":
        super().open(self.PATH)
        self.remove_ads()
        return self

    @allure.step("Seleccionar opción: Yes")
    def select_yes(self) -> "RadioButtonPage":
        self.js_click(self.YES_RADIO)
        return self

    @allure.step("Seleccionar opción: Impressive")
    def select_impressive(self) -> "RadioButtonPage":
        self.js_click(self.IMPRESSIVE_RADIO)
        return self

    # ── Getters ───────────────────────────────────────────────────────────────

    def get_selected_text(self) -> str:
        return self.get_text(self.OUTPUT_TEXT)

    def is_no_radio_disabled(self) -> bool:
        """El radio 'No' está deshabilitado en DemoQA por diseño."""
        no_input = self.find(self.NO_RADIO_INPUT)
        return not no_input.is_enabled()
