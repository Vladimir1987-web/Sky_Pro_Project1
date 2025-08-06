import json
import logging
from datetime import datetime

import pandas as pd

from src.utils import (conversion_currency, conversion_stocks, get_card_info, get_greetings, get_top_five_max_prices,
                       get_user_settings, read_date_as_df)

# Основная конфигурация logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=r"C:\Training\Python-development\Project\Sky_Pro_Project3\logs\views.log",
    encoding="utf-8",  # Запись логов в файл
    filemode="w",
)

app_logger = logging.getLogger("views.py")


def get_main_page_info(date: str) -> str:
    # Приветствие
    app_logger.info("Приветствие")
    greetings = get_greetings()

    app_logger.info("Чтение json-файла и фильтрация его по дате")
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
    app_logger.info("Вывод информации по картам")
    card_info = get_card_info(selected_transactions)

    # Топ-5 транзакций по сумме платежа
    app_logger.info("Вывод списка словарей топ-5 транзакций")
    top_five = get_top_five_max_prices(selected_transactions)

    # Курс валют и стоимость акций
    app_logger.info("Вывод словаря со списками валют и акций")
    stock_path = r"C:\Training\Python-development\Project\Sky_Pro_Project3\user_settings.json"
    stock_currencies = get_user_settings(stock_path)
    stocks = stock_currencies["user_stocks"]  # ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    currencies = stock_currencies["user_currencies"]  # ['USD', 'EUR']

    app_logger.info("Получение списков словарей со стоимостью акций курсом валют")
    conversion = conversion_currency(currencies)
    prices_stocks = conversion_stocks(stocks)

    result = {
        "greeting": greetings,
        "cards": card_info,
        "top_transactions": top_five,
        "currency_rates": conversion,
        "stock_prices": prices_stocks,
    }
    app_logger.info("Вывод информации в формате json")
    return json.dumps(result, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    print(get_main_page_info("2021-07-25 20:10:33"))
