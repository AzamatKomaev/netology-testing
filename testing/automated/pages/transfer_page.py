"""Page Object формы перевода F-Bank."""
from __future__ import annotations

from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


CARD_INPUT = (By.CSS_SELECTOR, "input[placeholder='0000 0000 0000 0000']")
AMOUNT_INPUT = (By.CSS_SELECTOR, "input[placeholder='1000']")
TRANSFER_BUTTON = (By.XPATH, "//button[normalize-space()='Перевести']")
INSUFFICIENT_FUNDS = (
    By.XPATH,
    "//*[normalize-space()='Недостаточно средств на счете']",
)
COMMISSION = (By.ID, "comission")

CURRENCY_TITLES = {"rub": "Рубли", "usd": "Доллары", "euro": "Евро"}


def _currency_card(title: str):
    return (
        By.XPATH,
        f"//*[@role='button'][.//h2[normalize-space()='{title}']]",
    )


class TransferPage:
    def __init__(self, driver: WebDriver, base_url: str):
        self.driver = driver
        self.base_url = base_url.rstrip("/")

    def open(self, balance: int = 10_000, reserved: int = 0) -> "TransferPage":
        url = f"{self.base_url}/?balance={balance}&reserved={reserved}"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[normalize-space()='F-Bank']")
            )
        )
        return self

    def select_currency(self, label: str) -> "TransferPage":
        title = CURRENCY_TITLES[label]
        card = WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(_currency_card(title))
        )
        card.click()
        WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(CARD_INPUT)
        )
        return self

    def enter_card_number(self, raw: str) -> "TransferPage":
        field = self.driver.find_element(*CARD_INPUT)
        field.click()
        field.send_keys(Keys.END)
        for _ in range(len(field.get_attribute("value") or "")):
            field.send_keys(Keys.BACK_SPACE)
        field.send_keys(raw)
        return self

    def card_field_value(self) -> str:
        return self.driver.find_element(*CARD_INPUT).get_attribute("value") or ""

    def card_digits(self) -> str:
        return "".join(ch for ch in self.card_field_value() if ch.isdigit())

    def enter_amount(self, raw: str) -> "TransferPage":
        field = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(AMOUNT_INPUT)
        )
        field.click()
        field.send_keys(Keys.END)
        # Стираем посимвольно через клавиатуру, чтобы каждый шаг прошёл через React onChange.
        max_len = len(field.get_attribute("value") or "") + 5
        for _ in range(max_len):
            field.send_keys(Keys.BACK_SPACE)
            if not (field.get_attribute("value") or ""):
                break
        field.send_keys(raw)
        return self

    def amount_field_value(self) -> str:
        return self.driver.find_element(*AMOUNT_INPUT).get_attribute("value") or ""

    def commission_text(self) -> str:
        try:
            return self.driver.find_element(*COMMISSION).text.strip()
        except NoSuchElementException:
            return ""

    def click_transfer(self) -> None:
        self.driver.find_element(*TRANSFER_BUTTON).click()

    def is_transfer_button_visible(self) -> bool:
        try:
            self.driver.find_element(*TRANSFER_BUTTON)
            return True
        except NoSuchElementException:
            return False

    def is_insufficient_funds_visible(self) -> bool:
        try:
            self.driver.find_element(*INSUFFICIENT_FUNDS)
            return True
        except NoSuchElementException:
            return False

    def wait_for_alert_text(self, timeout: int = 5) -> str:
        WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
        alert = self.driver.switch_to.alert
        text = alert.text
        alert.accept()
        return text

    def alert_present(self, timeout: int = 2) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False
