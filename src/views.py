import json
from datetime import datetime

import pandas as pd

from utils import (conversion_currency, conversion_stocks, get_card_info, get_greetings, get_top_five_max_prices,
                   get_user_settings, read_date_as_df)


def get_main_page_info(date: str) -> str:
    # Приветствие
    greetings = get_greetings()

    # Данные с начала месяца, на который выпадает входящая дата, по входящую дату.
    file_path = r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx"
    all_transactions = read_date_as_df(file_path)
    # Объекты datetime периода с начала месяца
    end_period = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    start_period = end_period.replace(day=1, hour=0, minute=0, second=0)

    selected_transactions = all_transactions[
        (pd.to_datetime(all_transactions["Дата операции"]) >= start_period)
        & (pd.to_datetime(all_transactions["Дата операции"]) <= end_period)
    ]

    # Информация по картам
    card_info = get_card_info(selected_transactions)

    # Топ-5 транзакций по сумме платежа
    top_five = get_top_five_max_prices(selected_transactions)

    # Курс валют
    stock_path = r"C:\Training\Python-development\Project\Sky_Pro_Project3\user_settings.json"
    stock_currencies = get_user_settings(stock_path)
    stocks = stock_currencies["user_stocks"]  # ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    currencies = stock_currencies["user_currencies"]  # ['USD', 'EUR']

    conversion = conversion_currency(currencies)
    prices_stocks = conversion_stocks(stocks)

    result = {
        "greeting": greetings,
        "cards": card_info,
        "top_transactions": top_five,
        "currency_rates": conversion,
        "stock_prices": prices_stocks,
    }

    return json.dumps(result, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print(get_main_page_info("2021-07-25 20:10:33"))
