import allure
import pytest

from pages.web_tables_page import WebTablesPage
from utils.data_generator import generate_person


@allure.epic("DemoQA - Elements")
@allure.feature("Web Tables")
class TestWebTables:

    @allure.story("Agregar nuevo registro")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.elements
    def test_add_new_record(self, driver):
        """
        DADO que el usuario está en la página Web Tables
        CUANDO agrega un nuevo registro con datos válidos
        ENTONCES el registro debe aparecer en la tabla
        """
        person = generate_person()
        page = WebTablesPage(driver)

        page.open()
        page.open_add_modal()
        page.fill_registration_form(
            first_name=person.first_name,
            last_name=person.last_name,
            email=person.email,
            age=person.age,
            salary=person.salary,
            department=person.department,
        )
        page.submit_form()

        allure.attach(
            (
                f"Nombre: {person.first_name} {person.last_name}\n"
                f"Email: {person.email}\n"
                f"Departamento: {person.department}"
            ),
            name="Datos del registro",
            attachment_type=allure.attachment_type.TEXT
        )

        assert page.is_value_in_table(person.first_name), (
            f"El nombre '{person.first_name}' no apareció en la tabla"
        )
        assert page.is_value_in_table(person.email), (
            f"El email '{person.email}' no apareció en la tabla"
        )

    @allure.story("Buscar registro por nombre")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.elements
    def test_search_filters_table(self, driver):
        """
        DADO que existe un registro con datos conocidos en la tabla
        CUANDO el usuario busca por el email
        ENTONCES solo deben aparecer filas que coincidan
        """
        person = generate_person()
        page = WebTablesPage(driver)

        # Primero agrega el registro
        page.open()
        page.open_add_modal()
        page.fill_registration_form(
            first_name=person.first_name,
            last_name=person.last_name,
            email=person.email,
            age=person.age,
            salary=person.salary,
            department=person.department,
        )
        page.submit_form()

        # Luego busca
        page.search(person.email)

        rows = page.get_all_rows_text()
        assert len(rows) >= 1, "La búsqueda no retornó resultados"
        assert all(person.email in row for row in rows), (
            "La tabla muestra filas que no coinciden con el filtro"
        )

    @allure.story("Eliminar un registro")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_delete_record(self, driver):
        """
        DADO que hay registros en la tabla
        CUANDO el usuario elimina el primer registro
        ENTONCES ese registro no debe aparecer en la tabla
        """
        page = WebTablesPage(driver)
        page.open()

        rows_before = page.get_visible_row_count()
        first_row_text = page.get_all_rows_text()[0]

        # Extraemos el email del primer registro para verificar después
        email_in_row = [cell for cell in first_row_text.split("\n") if "@" in cell]

        page.delete_row(row_index=0)

        rows_after = page.get_visible_row_count()
        assert rows_after == rows_before - 1, (
            f"Se esperaban {rows_before - 1} filas, pero hay {rows_after}"
        )
        if email_in_row:
            assert not page.is_value_in_table(email_in_row[0]), (
                "El registro eliminado sigue apareciendo en la tabla"
            )

    @allure.story("Editar un registro existente")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_edit_record(self, driver):
        """
        DADO que hay registros en la tabla
        CUANDO el usuario edita el primer registro con un nuevo salario
        ENTONCES la tabla debe reflejar el salario actualizado
        """
        new_salary = "999999"
        page = WebTablesPage(driver)

        page.open()
        page.click_edit(row_index=0)
        page.type(page.SALARY_INPUT, new_salary)
        page.submit_form()

        assert page.is_value_in_table(new_salary), (
            f"El salario actualizado '{new_salary}' no aparece en la tabla"
        )
