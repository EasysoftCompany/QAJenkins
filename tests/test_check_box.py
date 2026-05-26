import allure
import pytest

from pages.check_box_page import CheckBoxPage


@allure.epic("DemoQA - Elements")
@allure.feature("Check Box")
class TestCheckBox:

    @allure.story("Seleccionar Home completo")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.elements
    def test_select_home_shows_all_children(self, driver):
        """
        DADO que el usuario está en la página Check Box
        CUANDO selecciona el checkbox raíz 'Home'
        ENTONCES el panel de resultado debe incluir Home y todos sus hijos
        """
        page = CheckBoxPage(driver)
        page.open()
        page.select_home()

        selected = page.get_selected_items()

        assert page.is_result_visible(), "El panel de resultado no apareció"
        assert len(selected) > 0, "No se seleccionó ningún ítem"

        selected_lower = [item.lower() for item in selected]
        assert "home" in selected_lower
        assert "desktop" in selected_lower
        assert "documents" in selected_lower
        assert "downloads" in selected_lower

    @allure.story("Seleccionar solo Desktop")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_select_desktop_only(self, driver):
        """
        DADO que el árbol está expandido
        CUANDO el usuario selecciona solo 'Desktop'
        ENTONCES el resultado debe mostrar Desktop y sus hijos (Notes, Commands)
        """
        page = CheckBoxPage(driver)
        page.open()
        page.select_desktop()

        selected = page.get_selected_items()
        selected_lower = [item.lower() for item in selected]

        assert "desktop" in selected_lower
        assert "home" not in selected_lower, (
            "Home no debería estar seleccionado si solo elegimos Desktop"
        )

    @allure.story("Expandir y colapsar el árbol")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.regression
    @pytest.mark.elements
    def test_expand_and_collapse_tree(self, driver):
        """
        DADO que el usuario está en la página
        CUANDO expande y luego colapsa el árbol
        ENTONCES no debe quedar ningún ítem seleccionado en el resultado
        """
        page = CheckBoxPage(driver)
        page.open()
        page.expand_all()
        page.collapse_all()

        assert not page.is_result_visible(), (
            "El resultado apareció sin haber seleccionado ningún checkbox"
        )
