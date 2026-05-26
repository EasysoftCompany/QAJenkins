import allure
import pytest

from pages.radio_button_page import RadioButtonPage


@allure.epic("DemoQA - Elements")
@allure.feature("Radio Button")
class TestRadioButton:

    @allure.story("Selección de opción Yes")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.elements
    def test_select_yes_shows_correct_text(self, driver):
        """
        DADO que el usuario está en la página Radio Button
        CUANDO hace clic en 'Yes'
        ENTONCES el texto de confirmación debe ser 'Yes'
        """
        page = RadioButtonPage(driver)
        page.open()
        page.select_yes()

        result = page.get_selected_text()
        assert result == "Yes", f"Se esperaba 'Yes' pero se obtuvo '{result}'"

    @allure.story("Selección de opción Impressive")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_select_impressive_shows_correct_text(self, driver):
        """
        DADO que el usuario está en la página Radio Button
        CUANDO hace clic en 'Impressive'
        ENTONCES el texto de confirmación debe ser 'Impressive'
        """
        page = RadioButtonPage(driver)
        page.open()
        page.select_impressive()

        result = page.get_selected_text()
        assert result == "Impressive", f"Se esperaba 'Impressive' pero se obtuvo '{result}'"

    @allure.story("Radio 'No' está deshabilitado")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_no_radio_is_disabled(self, driver):
        """
        DADO que el usuario está en la página Radio Button
        CUANDO observa el radio button 'No'
        ENTONCES debe estar deshabilitado (comportamiento definido por DemoQA)
        """
        page = RadioButtonPage(driver)
        page.open()

        assert page.is_no_radio_disabled(), (
            "Se esperaba que el radio 'No' estuviera deshabilitado"
        )

    @allure.story("Cambio de selección entre radios")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_switch_selection_between_radios(self, driver):
        """
        DADO que el usuario seleccionó 'Yes'
        CUANDO cambia a 'Impressive'
        ENTONCES el output debe actualizarse a 'Impressive'
        """
        page = RadioButtonPage(driver)
        page.open()
        page.select_yes()

        assert page.get_selected_text() == "Yes"

        page.select_impressive()
        assert page.get_selected_text() == "Impressive"
