from datetime import datetime
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest
from pandas import DataFrame
from twelvedata import TDClient

from src.utils import (conversion_currency, conversion_stocks, get_card_info, get_greetings, get_top_five_max_prices,
                       get_user_settings, read_date_as_df)

"""Проверка функции get_greetings"""


@patch("src.utils.datetime")
def test_get_greetings(mock_get) -> None:
    mock_get.now.return_value = datetime.strptime("2025-08-04 21:02:27.481328", "%Y-%m-%d %H:%M:%S.%f")
    assert get_greetings() == "Добрый вечер!"


"""Проверка функции read_date_as_df"""


@pytest.fixture
def expected_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Дата операции": ["31.12.2021 16:44:00", "31.12.2021 16:42:04"],
            "Сумма операции с округлением": ["160.89", "64.00"],
        }
    )


def test_read_date_as_df(expected_dataframe) -> None:
    with patch("pandas.read_excel") as mock_read_excel:
        mock_read_excel.return_value = expected_dataframe
        actual_dataframe = read_date_as_df(
            r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx"
        )
        pd.testing.assert_frame_equal(actual_dataframe, expected_dataframe)


"""Проверка функции get_card_info"""


@pytest.fixture
def all_transactions() -> DataFrame:
    file_path = r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx"
    return read_date_as_df(file_path)


def test_get_card_info(all_transactions: DataFrame) -> None:
    assert get_card_info(all_transactions) == [
        {"last_digits": "1112", "total_spent": 46207.08, "cashback": 462.07},
        {"last_digits": "4556", "total_spent": 4144689.17, "cashback": 41446.89},
        {"last_digits": "5091", "total_spent": 19816.84, "cashback": 198.17},
        {"last_digits": "5441", "total_spent": 470854.8, "cashback": 4708.55},
        {"last_digits": "5507", "total_spent": 84000.0, "cashback": 840.0},
        {"last_digits": "6002", "total_spent": 69200.0, "cashback": 692.0},
        {"last_digits": "7197", "total_spent": 2557824.54, "cashback": 25578.25},
    ]


"""Проверка функции get_top_five_max_prices"""


def test_get_top_five_max_prices(all_transactions: DataFrame) -> None:
    assert get_top_five_max_prices(all_transactions) == [
        {
            "date": "21.03.2019",
            "amount": -190044.51,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "date": "28.07.2018",
            "amount": -179571.56,
            "category": np.nan,
            "description": "Перевод средств с брокерского счета",
        },
        {
            "date": "27.07.2018",
            "amount": -179571.56,
            "category": np.nan,
            "description": "Перевод средств с брокерского счета",
        },
        {
            "date": "27.07.2018",
            "amount": -179571.56,
            "category": np.nan,
            "description": "Перевод средств с брокерского счета",
        },
        {
            "date": "23.10.2018",
            "amount": -177506.03,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
    ]


"""Проверка функции get_user_settings"""


def test_get_user_settings() -> None:
    assert get_user_settings(r"C:\Training\Python-development\Project\Sky_Pro_Project3\user_settings.json") == {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"],
    }


"""Проверка функции conversion_currency"""


@patch("src.utils.requests.get")
def test_conversion_currency(mock_get) -> None:
    mock_get.return_value.json.return_value = {
        "success": True,
        "timestamp": 1752256276,
        "base": "USD",
        "date": "2025-07-11",
        "rates": {"RUB": 77.999},
    }

    assert conversion_currency(["USD"]) == [{"currency": "USD", "rate": 77.999}]


"""Проверка функции conversion_stocks"""


@patch("src.utils.TDClient.price")
def test_conversion_stocks(mock_get) -> None:
    mock_get.return_value.as_json = MagicMock(return_value={"price": "203.35001"})
    assert conversion_stocks(["AAPL"]) == [{"stock": "AAPL", "price": "203.35001"}]
