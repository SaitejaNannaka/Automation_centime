import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import yaml
import uuid
import os
from datetime import datetime


# Capture screenshot on test failure
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = item.funcargs.get('request').cls.driver
        screenshot_name = f"screenshot_{uuid.uuid4().hex[:8]}.png"
        screenshot_path = os.path.join("reports", "screenshots", screenshot_name)
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)

        driver.save_screenshot(screenshot_path)
        if "pytest_html" in item.config.pluginmanager.list_name_plugin():
            report.extra = report.extra or []
            report.extra.append(pytest_html.extras.png(screenshot_path))


# Update the email in data.yaml with a unique value before each test
def update_data_yaml(file_path='utils/data.yaml'):
    unique_email = f"saiteja_nannaka{uuid.uuid4().hex[:9]}@example.com"

    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)

        data['registration']['email'] = unique_email

        with open(file_path, 'w') as file:
            yaml.safe_dump(data, file)

        print(f"Updated email in YAML: {unique_email}")
    except Exception as e:
        pytest.fail(f"Failed to update data.yaml: {e}")

    return unique_email


# Fixture to update and reload data.yaml before each test
@pytest.fixture(scope="function")
def data():
    update_data_yaml()
    with open("utils/data.yaml", 'r') as file:
        return yaml.safe_load(file)


# Fixture to load config.yaml
@pytest.fixture(scope="session")
def config():
    try:
        with open("utils/config.yaml", 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        pytest.fail("config.yaml file not found.")
    except yaml.YAMLError as e:
        pytest.fail(f"Error reading config.yaml: {e}")


# Fixture to load locators.yaml
@pytest.fixture(scope="session")
def locators():
    try:
        with open("utils/locators.yaml", 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        pytest.fail("locators.yaml file not found.")
    except yaml.YAMLError as e:
        pytest.fail(f"Error reading locators.yaml: {e}")


# Fixture to set up WebDriver
@pytest.fixture(scope="function")
def setup(request, config, locators, data):
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.maximize_window()
        request.cls.driver = driver
        request.cls.config = config
        request.cls.locators = locators
        request.cls.data = data
        yield
    except Exception as e:
        pytest.fail(f"Failed to initialize WebDriver: {e}")
    finally:
        driver.quit()


# Customize pytest-html report metadata
def pytest_configure(config):
    if config.pluginmanager.hasplugin('html'):
        if hasattr(config, '_metadata'):
            config._metadata.clear()
            config._metadata['Project Name'] = 'Centime Automation'
            config._metadata['Module Name'] = 'Shop'
            config._metadata['Tester'] = 'Saiteja Nannaka'
        else:
            print("Warning: _metadata attribute is not available. Metadata will not be added to the report.")
    else:
        print("Warning: pytest-html plugin is not installed. Metadata will not be added to the report.")


# Customize the pytest-html report title
@pytest.hookimpl(tryfirst=True)
def pytest_html_report_title(report):
    report.title = "Centime Automation Test Report"


# Add custom information to the pytest-html report summary
@pytest.hookimpl(tryfirst=True)
def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([pytest_html.extras.html('<p>Project: Centime Automation</p>'),
                   pytest_html.extras.html(f'<p>Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>')])
