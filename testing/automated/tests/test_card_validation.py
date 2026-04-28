"""TC-03 / BUG-002: поле номера карты должно ограничивать ввод 16 цифрами."""
import pytest

from pages.transfer_page import TransferPage


@pytest.mark.bug
def test_card_number_max_length_is_16_digits(driver, base_url):
    page = (
        TransferPage(driver, base_url)
        .open(balance=10_000, reserved=0)
        .select_currency("rub")
        .enter_card_number("12345678123456789")
    )

    digits = page.card_digits()
    assert len(digits) == 16, (
        f"Поле приняло {len(digits)} цифр (значение: {page.card_field_value()!r}). "
        "Ожидается ограничение до 16."
    )
