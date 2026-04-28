"""TC-04 / BUG-001: поле суммы перевода не должно принимать отрицательные значения."""
import pytest

from pages.transfer_page import TransferPage


@pytest.mark.bug
def test_negative_amount_must_be_rejected(driver, base_url):
    page = (
        TransferPage(driver, base_url)
        .open(balance=10_000, reserved=0)
        .select_currency("rub")
        .enter_card_number("1234567812345678")
        .enter_amount("-100")
    )

    value = page.amount_field_value()
    assert not value.startswith("-"), (
        f"Поле суммы сохраняет знак минус: {value!r}. "
        "Ожидается, что отрицательные суммы будут отвергнуты на этапе ввода."
    )

    if page.is_transfer_button_visible():
        page.click_transfer()
        if page.alert_present(timeout=2):
            pytest.fail(
                "Перевод с отрицательной суммой принят банком (BUG-001)."
            )
