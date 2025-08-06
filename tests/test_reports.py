import pandas as pd

from src.reports import spending_by_category

"""Проверка функции spending_by_category"""


def test_spending_by_category() -> None:
    mock_data = pd.DataFrame(
        {
            "Дата операции": ["2018-05-25 20:10:33", "2018-07-25 20:10:33"],
            "Категория": ["Food", "Transport"],
            "Сумма операции": [-100, -50],
        }
    )

    # Устанавливаем временные рамки и категорию для фильтрации
    start_dt = pd.to_datetime("2018-05-25 20:10:33")
    date_dt = pd.to_datetime("2018-07-25 20:10:33")
    category = "Food"
    mock_data["Дата операции"] = pd.to_datetime(mock_data["Дата операции"])

    # Выполняем фильтрацию с тестовыми данными
    selected_transactions = mock_data[
        (mock_data["Дата операции"] >= start_dt)
        & (mock_data["Дата операции"] <= date_dt)
        & (mock_data["Категория"] == category)
        & (mock_data["Сумма операции"] < 0)
    ]

    assert selected_transactions.equals(spending_by_category(mock_data, "Food", "2018-07-25 20:10:33"))
