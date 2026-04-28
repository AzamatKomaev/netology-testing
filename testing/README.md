# Тестирование F-Bank

Дипломное задание по дисциплине "Тестирование прикладного ПО" (Нетология).
Объект тестирования - учебное веб-приложение **F-Bank**, форма перевода денег со счёта на карту.

## Структура каталога

```
azamat:testing/ (main) $ tree
.
├── automated
│   ├── conftest.py
│   ├── pages
│   │   ├── __init__.py
│   │   └── transfer_page.py
│   ├── pytest.ini
│   ├── requirements.txt
│   └── tests
│       ├── __init__.py
|       ├── test_successful_transfer.py   (TC-01, проходит)
|       ├── test_insufficient_funds.py    (TC-02, проходит)
|       ├── test_negative_amount.py       (TC-04, падает - BUG-001)
|       ├── test_card_validation.py       (TC-03, падает - BUG-002)
|       └── test_currency_balance.py      (TC-05, падает - BUG-003)
├── manual
│   ├── bug-reports
│   │   ├── BUG-001-negative-amount.md
│   │   ├── BUG-002-card-17-digits.md
│   │   └── BUG-003-currency-mismatch.md
│   ├── test-cases.md  - 5 тест-кейсов с результатами прогонa
│   └── test-plan.md   - тест-план
└── README.md  - этот файл

```

## Как поднять приложение

Из корня репозитория:

```bash
python3 -m http.server 8000 --directory dist
```

Открыть `http://localhost:8000/?balance=10000&reserved=0` (параметры
URL задают рублёвый баланс и сумму резерва).

## Ручное тестирование

См. [manual/test-plan.md](manual/test-plan.md) и
[manual/test-cases.md](manual/test-cases.md). Прогон включает 5 тест-кейсов,
3 из которых выявляют дефекты, описанные в `manual/bug-reports/`.

### Найденные дефекты

| ID | Severity | Заголовок |
|----|----------|-----------|
| [BUG-001](manual/bug-reports/BUG-001-negative-amount.md) | Critical | Поле "Сумма перевода" принимает отрицательные значения |
| [BUG-002](manual/bug-reports/BUG-002-card-17-digits.md) | Major    | Поле "Номер карты" допускает ввод 17 цифр |
| [BUG-003](manual/bug-reports/BUG-003-currency-mismatch.md) | Critical | Проверка достаточности средств всегда использует рублёвый счёт |

Эти же дефекты заведены как GitHub Issues в репозитории - см. вкладку
[Issues](../../issues?q=is%3Aissue+label%3Abug). Шаблон новых багов:
[`.github/ISSUE_TEMPLATE/bug_report.yml`](../.github/ISSUE_TEMPLATE/bug_report.yml).

## Автоматизированные тесты

Selenium 4 + pytest. Драйвер устанавливается автоматически через
встроенный Selenium Manager (отдельная установка chromedriver не требуется).

### Локальный запуск

```bash
# 1. Поднять приложение в отдельном терминале
python3 -m http.server 8000 --directory dist

# 2. В другом терминале - установить зависимости и прогнать тесты
cd testing/automated
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

Параметры окружения:

| Переменная | Значение по умолчанию | Описание |
|------------|------------------------|----------|
| `APP_URL`  | `http://localhost:8000` | URL приложения |
| `BROWSER`  | `chrome`               | `chrome` или `firefox` |
| `HEADLESS` | `1`                    | `0` - запуск с UI |

### Ожидаемый результат прогона

```
tests/test_card_validation.py::test_card_number_max_length_is_16_digits FAILED
tests/test_currency_balance.py::test_usd_balance_check_uses_usd_account  FAILED
tests/test_insufficient_funds.py::test_insufficient_funds_message_displayed PASSED
tests/test_negative_amount.py::test_negative_amount_must_be_rejected     FAILED
tests/test_successful_transfer.py::test_successful_rub_transfer          PASSED

3 failed, 2 passed
```

Падения - это **намеренное** поведение тестов: они проверяют ОЖИДАЕМОЕ
(корректное) поведение продукта, поэтому будут красными до тех пор,
пока разработчики не починят BUG-001 / BUG-002 / BUG-003.

## CI

Workflow `.github/workflows/selenium.yml` запускается на каждый
`push` и `pull_request` в `main`:

1. поднимает Python 3.12 на `ubuntu-latest`;
2. устанавливает зависимости из `testing/automated/requirements.txt`;
3. запускает `python -m http.server 8000 --directory dist` в фоне;
4. прогоняет `pytest` в Chrome (headless);
5. публикует JUnit-отчёт.

Сборка должна быть **красной**, поскольку 3 из 5 тестов выявляют
неисправленные дефекты - это соответствует требованию задания.
