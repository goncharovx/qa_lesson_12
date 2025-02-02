import os

import pytest
from dotenv import load_dotenv
from selene import browser
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from utils import attach

login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
selenoid_url = os.getenv('SELENOID_URL')
DEFAULT_BROWSER_VERSION = "125.0"


def pytest_addoption(parser):
    parser.addoption('--browser_version', default='125.0')
    parser.addoption('--browser_type')


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()
    assert os.getenv("SELENOID_URL"), " Ошибка: Переменная окружения SELENOID_URL не задана!"
    assert os.getenv("LOGIN"), " Ошибка: Переменная окружения LOGIN не задана!"
    assert os.getenv("PASSWORD"), " Ошибка: Переменная окружения PASSWORD не задана!"


@pytest.fixture(scope='function')
def setup_browser(request):
    browser_version = request.config.getoption('--browser_version')
    browser_type = request.config.getoption('--browser_type')
    browser_version = browser_version if browser_version != "" else DEFAULT_BROWSER_VERSION

    options = Options()
    selenoid_capabilities = {
        "browserName": browser_type,
        "browserVersion": browser_version,
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True,
            "setSize": (1280, 1024)
        }
    }

    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://user1:1234@selenoid.autotests.cloud/wd/hub",
        options=options,
        keep_alive=True
    )

    browser.config.driver = driver

    driver_options = webdriver.ChromeOptions()

    driver_options.page_load_strategy = 'eager'
    driver_options.add_argument('--ignore-certificate-errors')
    browser.config.driver_options = driver_options

    browser.config.window_width = 1280
    browser.config.window_height = 724

    browser.config.base_url = 'https://demoqa.com'

    yield browser

    attach.add_html(browser)
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_video(browser)
    browser.quit()
