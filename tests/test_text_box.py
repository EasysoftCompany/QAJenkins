import allure
import pytest

from pages.text_box_page import TextBoxPage
from utils.data_generator import generate_person


@allure.epic("DemoQA - Elements")
@allure.feature("Text Box")
class TestTextBox:

    @allure.story("Envío de formulario válido")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.elements
    def test_fill_and_submit_full_form(self, driver):
        """
        DADO que el usuario está en la página Text Box
        CUANDO llena todos los campos con datos válidos y hace submit
        ENTONCES el panel de output debe mostrar los datos ingresados
        """
        person = generate_person()
        page = TextBoxPage(driver)

        page.open()
        page.fill_form(
            full_name=person.full_name,
            email=person.email,
            current_address=person.current_address,
            permanent_address=person.permanent_address,
        )
        page.submit()

        allure.attach(
            f"Nombre: {person.full_name}\nEmail: {person.email}",
            name="Datos del test",
            attachment_type=allure.attachment_type.TEXT
        )

        assert page.is_output_visible(), "El panel de output no apareció tras el submit"
        assert person.full_name in page.get_output_name()
        assert person.email in page.get_output_email()
        assert person.current_address in page.get_output_current_address()
        assert person.permanent_address in page.get_output_permanent_address()

    @allure.story("Email inválido no muestra output")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_invalid_email_does_not_show_output(self, driver):
        """
        DADO que el usuario está en la página Text Box
        CUANDO ingresa un email con formato inválido y hace submit
        ENTONCES el panel de output NO debe aparecer
        """
        page = TextBoxPage(driver)
        page.open()
        page.fill_form(
            full_name="QA Tester",
            email="correo-invalido-sin-arroba",
            current_address="Calle Falsa 123",
            permanent_address="Av. Siempre Viva 742",
        )
        page.submit()

        assert not page.is_output_visible(), (
            "El output apareció con un email inválido — el formulario debería rechazarlo"
        )

    @allure.story("Submit solo con nombre")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_submit_with_only_name(self, driver):
        """
        DADO que el usuario solo llena el campo nombre
        CUANDO hace submit
        ENTONCES el output debe mostrar únicamente el nombre
        """
        page = TextBoxPage(driver)
        page.open()
        page.type(page.FULL_NAME_INPUT, "Solo Nombre")
        page.submit()

        assert page.is_output_visible()
        assert "Solo Nombre" in page.get_output_name()
