import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from utils import attach

load_dotenv()

selenoid_url = os.getenv('SELENOID_URL')
user = os.getenv('LOGIN')
password = os.getenv('PASSWORD')


def pytest_addoption(parser):
    parser.addoption("--browser_type", action="store", default="chrome", help="Тип браузера (chrome или firefox)")
    parser.addoption("--browser_version", action="store", default="latest", help="Версия браузера")


@pytest.fixture(scope="function")
def setup_browser(request):
    browser_type = request.config.getoption("--browser_type").lower()
    browser_version = request.config.getoption("--browser_version")

    command_executor_url = f"https://{user}:{password}@{selenoid_url}/wd/hub"
    print(f"Command Executor URL: {command_executor_url}")

    if browser_type == 'chrome':
        options = ChromeOptions()
        options.add_argument("--ignore-certificate-errors")
        capabilities = {
            "browserName": "chrome",
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "screenResolution": "1280x1024x24"
            }
        }
        options.set_capability("selenoid:options", capabilities)

    elif browser_type == 'firefox':
        options = FirefoxOptions()
        options.set_preference("security.insecure_field_warning.contextual.enabled", False)
        capabilities = {
            "browserName": "firefox",
            "browserVersion": browser_version,
            "selenoid:options": {
                "enableVNC": True,
                "enableVideo": True,
                "screenResolution": "1280x1024x24"
            }
        }
        options.set_capability("selenoid:options", capabilities)

    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")

    driver = webdriver.Remote(
        command_executor=command_executor_url,
        options=options,
        keep_alive=True
    )

    browser.config.driver = driver
    browser.config.window_width = 1280
    browser.config.window_height = 724
    browser.config.base_url = 'https://demoqa.com'

    yield browser

    attach.add_logs(browser, request.config.getoption("--browser_type"))
    attach.add_screenshot(browser)
    attach.add_html(browser)
    attach.add_video(browser)
    browser.quit()
