"""TC-01: успешный перевод в рублях с достаточным остатком."""
from pages.transfer_page import TransferPage


def test_successful_rub_transfer(driver, base_url):
    page = (
        TransferPage(driver, base_url)
        .open(balance=10_000, reserved=0)
        .select_currency("rub")
        .enter_card_number("1234567812345678")
        .enter_amount("1000")
    )

    assert page.is_transfer_button_visible(), (
        'Кнопка "Перевести" должна быть видна при достаточном остатке'
    )
    assert not page.is_insufficient_funds_visible()

    page.click_transfer()
    text = page.wait_for_alert_text()
    assert "1000" in text and "1234567812345678" in text, (
        f"Неожиданный текст alert: {text!r}"
    )
