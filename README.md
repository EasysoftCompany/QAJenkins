# QA Automation Framework — DemoQA

Framework de automatización UI construido con **Python + Pytest + Selenium + Allure**.

## Tecnologías

| Herramienta | Rol |
|---|---|
| Python 3.11+ | Lenguaje base |
| Pytest | Runner y organización de tests |
| Selenium 4 | Automatización de navegador |
| Allure | Reportes HTML interactivos |
| webdriver-manager | Gestión automática de drivers |
| Faker | Generación de datos de prueba |
| python-dotenv | Configuración por ambiente |

## Estructura del proyecto

```
qa_automation/
├── config/
│   └── settings.py          # Variables de entorno y configuración global
├── pages/
│   ├── base_page.py         # Métodos comunes de Selenium + Allure
│   ├── text_box_page.py
│   ├── check_box_page.py
│   ├── radio_button_page.py
│   └── web_tables_page.py
├── tests/
│   ├── conftest.py          # Fixtures del browser y hooks de Allure
│   ├── test_text_box.py
│   ├── test_check_box.py
│   ├── test_radio_button.py
│   └── test_web_tables.py
├── utils/
│   └── data_generator.py    # Generador de datos con Faker
├── reports/
│   └── allure-results/      # Resultados crudos de Allure (auto-generado)
├── .env.example
├── pytest.ini
└── requirements.txt
```

## Setup inicial

### 1. Clonar y crear entorno virtual

```bash
git clone <repo-url>
cd qa_automation
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Instalar Allure CLI

```bash
# macOS
brew install allure

# Windows (con Scoop)
scoop install allure

# Linux
sudo apt-get install allure
```

### 4. Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env si se necesita cambiar browser, URL o headless
```

## Ejecución de tests

### Correr todos los tests

```bash
pytest
```

### Correr por marcador

```bash
pytest -m smoke          # Solo pruebas críticas
pytest -m regression     # Suite de regresión
pytest -m elements       # Solo sección Elements
```

### Correr en modo headless

```bash
HEADLESS=true pytest
```

### Correr con Firefox

```bash
pytest --browser=firefox
```

### Ejecución paralela

```bash
pytest -n 4              # 4 workers en paralelo
```

## Reportes Allure

### Generar y abrir reporte

```bash
allure serve reports/allure-results
```

### Generar reporte estático

```bash
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

## Convenciones del proyecto

- **Page Object Model**: cada página tiene su propia clase en `/pages`
- **Allure steps**: cada acción relevante usa `@allure.step`
- **Marcadores**: todo test tiene al menos un marcador de severidad y uno funcional
- **Naming**: tests con formato `test_<acción>_<resultado_esperado>`
- **Datos**: siempre usar `generate_person()` para datos dinámicos, nunca hardcoding
