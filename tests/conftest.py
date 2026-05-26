import allure
import pytest
from selenium import webdriver

from config.settings import BROWSER, HEADLESS


# ── Browser Factory ────────────────────────────────────────────────────────────

def _get_chrome_driver(headless: bool = False) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=options)


def _get_firefox_driver(headless: bool = False) -> webdriver.Firefox:
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("--headless")
    return webdriver.Firefox(options=options)


# ── Fixtures ───────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver(request):
    """
    Fixture principal del navegador.
    - Scope 'function': instancia nueva por cada test (aislamiento total).
    - Toma screenshot automático si el test falla.
    - Adjunta URL y título al reporte Allure.

    Prioridad de configuración: CLI > .env > default
    """
    browser = request.config.getoption("--browser")
    cli_headless = request.config.getoption("--headless")

    # CLI tiene prioridad; si no se pasó --headless, cae al valor del .env
    headless = cli_headless or HEADLESS

    if browser.lower() == "firefox":
        _driver = _get_firefox_driver(headless)
    else:
        _driver = _get_chrome_driver(headless)

    _driver.implicitly_wait(0)  # Usamos explicit waits en BasePage
    _driver.maximize_window()

    yield _driver

    # ── Teardown: captura info si el test falló ────────────────────────────
    if request.node.rep_call.failed if hasattr(request.node, "rep_call") else False:
        allure.attach(
            _driver.get_screenshot_as_png(),
            name="failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )
        allure.attach(
            _driver.current_url,
            name="URL al momento del fallo",
            attachment_type=allure.attachment_type.TEXT
        )

    _driver.quit()


@pytest.fixture(scope="session", autouse=True)
def allure_environment(tmp_path_factory):
    """Escribe el archivo environment.properties para el reporte Allure."""
    from pathlib import Path
    from config.settings import BASE_URL, BROWSER, HEADLESS

    env_path = Path("reports/allure-results/environment.properties")
    env_path.parent.mkdir(parents=True, exist_ok=True)
    env_path.write_text(
        f"Browser={BROWSER}\n"
        f"Headless={HEADLESS}\n"
        f"Base.URL={BASE_URL}\n"
        f"Framework=Selenium + Pytest\n"
        f"Language=Python\n"
    )


# ── Hooks ──────────────────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook para que el fixture 'driver' pueda saber si el test falló."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default=BROWSER,
        help="Navegador a usar: chrome | firefox"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Correr el navegador en modo headless (sin UI)"
    )