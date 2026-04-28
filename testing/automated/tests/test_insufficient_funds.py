"""TC-02: при недостатке средств кнопка скрыта, выводится сообщение."""
from pages.transfer_page import TransferPage


def test_insufficient_funds_message_displayed(driver, base_url):
    page = (
        TransferPage(driver, base_url)
        .open(balance=500, reserved=0)
        .select_currency("rub")
        .enter_card_number("1234567812345678")
        .enter_amount("1000")
    )

    assert page.is_insufficient_funds_visible(), (
        'Должно отображаться сообщение "Недостаточно средств на счете"'
    )
    assert not page.is_transfer_button_visible(), (
        'Кнопка "Перевести" должна быть скрыта'
    )
