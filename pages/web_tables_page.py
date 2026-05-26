import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class WebTablesPage(BasePage):
    PATH = "/webtables"

    # ── Locators ─────────────────────────────────────────────────────────────

    # Tabla y búsqueda
    ADD_BUTTON = (By.ID, "addNewRecordButton")
    SEARCH_INPUT = (By.ID, "searchBox")
    TABLE_ROWS = (By.CSS_SELECTOR, ".rt-tbody .rt-tr-group")
    TABLE_CELLS = (By.CSS_SELECTOR, ".rt-tbody .rt-td")

    # Modal de formulario
    FIRST_NAME_INPUT = (By.ID, "firstName")
    LAST_NAME_INPUT = (By.ID, "lastName")
    EMAIL_INPUT = (By.ID, "userEmail")
    AGE_INPUT = (By.ID, "age")
    SALARY_INPUT = (By.ID, "salary")
    DEPARTMENT_INPUT = (By.ID, "department")
    SUBMIT_BUTTON = (By.ID, "submit")

    # Acciones por fila
    EDIT_BUTTONS = (By.CSS_SELECTOR, "span[title='Edit']")
    DELETE_BUTTONS = (By.CSS_SELECTOR, "span[title='Delete']")

    # ── Actions ───────────────────────────────────────────────────────────────

    @allure.step("Abrir página Web Tables")
    def open(self) -> "WebTablesPage":
        super().open(self.PATH)
        self.remove_ads()
        return self

    @allure.step("Abrir modal de nuevo registro")
    def open_add_modal(self) -> "WebTablesPage":
        self.click(self.ADD_BUTTON)
        return self

    @allure.step("Llenar formulario del modal")
    def fill_registration_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        age: int,
        salary: int,
        department: str
    ) -> "WebTablesPage":
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.type(self.EMAIL_INPUT, email)
        self.type(self.AGE_INPUT, str(age))
        self.type(self.SALARY_INPUT, str(salary))
        self.type(self.DEPARTMENT_INPUT, department)
        return self

    @allure.step("Confirmar formulario")
    def submit_form(self) -> "WebTablesPage":
        self.click(self.SUBMIT_BUTTON)
        return self

    @allure.step("Buscar en tabla: '{keyword}'")
    def search(self, keyword: str) -> "WebTablesPage":
        self.type(self.SEARCH_INPUT, keyword)
        return self

    @allure.step("Eliminar la fila número {row_index}")
    def delete_row(self, row_index: int = 0) -> "WebTablesPage":
        delete_btns = self.find_all(self.DELETE_BUTTONS)
        delete_btns[row_index].click()
        return self

    @allure.step("Editar la fila número {row_index}")
    def click_edit(self, row_index: int = 0) -> "WebTablesPage":
        edit_btns = self.find_all(self.EDIT_BUTTONS)
        edit_btns[row_index].click()
        return self

    # ── Getters ───────────────────────────────────────────────────────────────

    def get_all_rows_text(self) -> list[str]:
        """Retorna el texto de todas las celdas no vacías de la tabla."""
        rows = self.find_all(self.TABLE_ROWS)
        return [row.text.strip() for row in rows if row.text.strip()]

    def is_value_in_table(self, value: str) -> bool:
        """Verifica si un valor está presente en cualquier celda de la tabla."""
        rows_text = self.get_all_rows_text()
        return any(value in row for row in rows_text)

    def get_visible_row_count(self) -> int:
        rows = self.find_all(self.TABLE_ROWS)
        return sum(1 for row in rows if row.text.strip())
