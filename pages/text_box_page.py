import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class TextBoxPage(BasePage):
    PATH = "/text-box"

    # ── Locators ─────────────────────────────────────────────────────────────
    FULL_NAME_INPUT = (By.ID, "userName")
    EMAIL_INPUT = (By.ID, "userEmail")
    CURRENT_ADDRESS_INPUT = (By.ID, "currentAddress")
    PERMANENT_ADDRESS_INPUT = (By.ID, "permanentAddress")
    SUBMIT_BUTTON = (By.ID, "submit")

    OUTPUT_SECTION = (By.ID, "output")
    OUTPUT_NAME = (By.CSS_SELECTOR, "#output #name")
    OUTPUT_EMAIL = (By.CSS_SELECTOR, "#output #email")
    OUTPUT_CURRENT_ADDRESS = (By.CSS_SELECTOR, "#output #currentAddress")
    OUTPUT_PERMANENT_ADDRESS = (By.CSS_SELECTOR, "#output #permanentAddress")

    # ── Actions ───────────────────────────────────────────────────────────────

    @allure.step("Abrir página Text Box")
    def open(self) -> "TextBoxPage":
        super().open(self.PATH)
        self.remove_ads()
        return self

    @allure.step("Llenar formulario: nombre='{full_name}', email='{email}'")
    def fill_form(
        self,
        full_name: str,
        email: str,
        current_address: str,
        permanent_address: str
    ) -> "TextBoxPage":
        self.type(self.FULL_NAME_INPUT, full_name)
        self.type(self.EMAIL_INPUT, email)
        self.type(self.CURRENT_ADDRESS_INPUT, current_address)
        self.type(self.PERMANENT_ADDRESS_INPUT, permanent_address)
        return self

    @allure.step("Hacer submit del formulario")
    def submit(self) -> "TextBoxPage":
        self.scroll_and_click(self.SUBMIT_BUTTON)
        return self

    # ── Getters ───────────────────────────────────────────────────────────────

    def is_output_visible(self) -> bool:
        return self.is_visible(self.OUTPUT_SECTION)

    def get_output_name(self) -> str:
        return self.get_text(self.OUTPUT_NAME)

    def get_output_email(self) -> str:
        return self.get_text(self.OUTPUT_EMAIL)

    def get_output_current_address(self) -> str:
        return self.get_text(self.OUTPUT_CURRENT_ADDRESS)

    def get_output_permanent_address(self) -> str:
        return self.get_text(self.OUTPUT_PERMANENT_ADDRESS)
