"""TC-05 / BUG-003: проверка остатка должна учитывать выбранную валюту."""
import pytest

from pages.transfer_page import TransferPage


@pytest.mark.bug
def test_usd_balance_check_uses_usd_account(driver, base_url):
    page = (
        TransferPage(driver, base_url)
        .open(balance=0, reserved=0)
        .select_currency("usd")
        .enter_card_number("1234567812345678")
        .enter_amount("50")
    )

    assert not page.is_insufficient_funds_visible(), (
        "При остатке USD = 100 usd перевод 50 usd должен быть разрешён, "
        "но приложение жалуется на недостаток средств - проверка "
        "использует рублёвый счёт (BUG-003)."
    )
    assert page.is_transfer_button_visible(), (
        'Кнопка "Перевести" должна отображаться при достаточном '
        "остатке на выбранной валютной карточке."
    )
