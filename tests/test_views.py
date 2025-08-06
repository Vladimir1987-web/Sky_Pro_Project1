import json
from unittest.mock import patch

import pandas as pd

from src.views import get_main_page_info


@patch("src.views.conversion_stocks")
@patch("src.views.conversion_currency")
@patch("src.views.get_user_settings")
@patch("src.views.get_top_five_max_prices")
@patch("src.views.get_card_info")
@patch("src.views.read_date_as_df")
@patch("src.views.get_greetings")
def test_get_main_page_info(
    mock_get_greeting,
    mock_read_date_as_df,
    mock_get_card_info,
    mock_get_top_five_max_prices,
    mock_get_user_settings,
    mock_conversion_currency,
    mock_conversion_stocks,
):
    mock_get_greeting.return_value = "Доброе утро!"
    mock_read_date_as_df.return_value = pd.DataFrame(
        {"Дата операции": ["2021-07-25 20:10:33", "2021-07-26 20:10:33", "2021-07-27 20:10:33"]}
    )
    mock_get_card_info.return_value = [{"last_digits": "**1234", "total_spent": 1000, "cashback": 100}]
    mock_get_top_five_max_prices.return_value = [
        {"date": "2021-07-25", "amount": 1000, "category": "Фастфуд", "description": "Кафе"}
    ]
    mock_get_user_settings.return_value = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }
    mock_conversion_currency.return_value = [{"currency": "USD", "rate": 1.0}, {"currency": "EUR", "rate": 0.8}]
    mock_conversion_stocks.return_value = [{"stock": "AAPL", "price": 100}, {"stock": "AMZN", "price": 150}]

    result = get_main_page_info("2021-07-25 20:10:33")
    expected = {
        "greeting": "Доброе утро!",
        "cards": [{"last_digits": "**1234", "total_spent": 1000, "cashback": 100}],
        "top_transactions": [{"date": "2021-07-25", "amount": 1000, "category": "Фастфуд", "description": "Кафе"}],
        "currency_rates": [{"currency": "USD", "rate": 1.0}, {"currency": "EUR", "rate": 0.8}],
        "stock_prices": [{"stock": "AAPL", "price": 100}, {"stock": "AMZN", "price": 150}],
    }
    assert result == json.dumps(expected, indent=4, ensure_ascii=False)
