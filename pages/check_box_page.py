import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckBoxPage(BasePage):
    PATH = "/checkbox"

    # ── Locators ─────────────────────────────────────────────────────────────
    EXPAND_ALL_BUTTON = (By.CSS_SELECTOR, "button[title='Expand all']")
    COLLAPSE_ALL_BUTTON = (By.CSS_SELECTOR, "button[title='Collapse all']")

    HOME_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='tree-node-home']")
    DESKTOP_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='tree-node-desktop']")
    DOCUMENTS_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='tree-node-documents']")
    DOWNLOADS_CHECKBOX_LABEL = (By.CSS_SELECTOR, "label[for='tree-node-downloads']")

    OUTPUT_ITEMS = (By.CSS_SELECTOR, ".check-box-table-list .text-success")
    RESULT_SECTION = (By.CSS_SELECTOR, "#result")

    # ── Actions ───────────────────────────────────────────────────────────────

    @allure.step("Abrir página Check Box")
    def open(self) -> "CheckBoxPage":
        super().open(self.PATH)
        self.remove_ads()
        return self

    @allure.step("Expandir todos los nodos")
    def expand_all(self) -> "CheckBoxPage":
        self.click(self.EXPAND_ALL_BUTTON)
        return self

    @allure.step("Colapsar todos los nodos")
    def collapse_all(self) -> "CheckBoxPage":
        self.click(self.COLLAPSE_ALL_BUTTON)
        return self

    @allure.step("Seleccionar checkbox: Home")
    def select_home(self) -> "CheckBoxPage":
        self.js_click(self.HOME_CHECKBOX_LABEL)
        return self

    @allure.step("Seleccionar checkbox: Desktop")
    def select_desktop(self) -> "CheckBoxPage":
        self.expand_all()
        self.js_click(self.DESKTOP_CHECKBOX_LABEL)
        return self

    @allure.step("Seleccionar checkbox: Documents")
    def select_documents(self) -> "CheckBoxPage":
        self.expand_all()
        self.js_click(self.DOCUMENTS_CHECKBOX_LABEL)
        return self

    @allure.step("Seleccionar checkbox: Downloads")
    def select_downloads(self) -> "CheckBoxPage":
        self.expand_all()
        self.js_click(self.DOWNLOADS_CHECKBOX_LABEL)
        return self

    # ── Getters ───────────────────────────────────────────────────────────────

    def get_selected_items(self) -> list[str]:
        """Retorna los nombres de los ítems marcados en el panel de resultado."""
        elements = self.find_all(self.OUTPUT_ITEMS)
        return [el.text for el in elements]

    def is_result_visible(self) -> bool:
        return self.is_visible(self.RESULT_SECTION)
