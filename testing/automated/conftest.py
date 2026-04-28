"""
Фикстуры pytest для Selenium-тестов F-Bank.

Переменные окружения:
- BROWSER:  chrome (по умолчанию) или firefox
- HEADLESS: 0 для запуска с UI, иначе headless
- APP_URL:  URL приложения (по умолчанию http://localhost:8000)
"""
from __future__ import annotations

import os
import sys

import pytest
from selenium import webdriver

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(scope="session")
def base_url() -> str:
    return os.environ.get("APP_URL", "http://localhost:8000")


def _build_driver():
    browser = os.environ.get("BROWSER", "chrome").lower()
    headless = os.environ.get("HEADLESS", "1") != "0"

    if browser == "firefox":
        from selenium.webdriver.firefox.options import Options

        opts = Options()
        if headless:
            opts.add_argument("--headless")
        opts.add_argument("--width=1280")
        opts.add_argument("--height=900")
        return webdriver.Firefox(options=opts)

    from selenium.webdriver.chrome.options import Options

    opts = Options()
    if headless:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument("--disable-gpu")
    return webdriver.Chrome(options=opts)


@pytest.fixture
def driver():
    drv = _build_driver()
    drv.set_page_load_timeout(20)
    yield drv
    drv.quit()
