import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv
from pandas import DataFrame
from twelvedata import TDClient


def get_greetings() -> str:
    """Приветствие"""
    current_date_time = datetime.now()
    hour = current_date_time.hour
    if hour > 0 and hour <= 6:
        return "Доброй ночи!"
    elif hour > 6 and hour < 12:
        return "Доброе утро!"
    elif hour >= 12 and hour <= 18:
        return "Добрый день!"
    elif hour > 18 and hour < 24:
        return "Добрый вечер!"


def read_date_as_df(path: str) -> DataFrame:
    """Считывает информацию из excel"""
    df = pd.read_excel(path, dtype={"Дата операции": "object"})
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    return df


def get_card_info(data: DataFrame) -> list:
    """Выводит список словарей с информацией по картам"""
    last_digits = data["Номер карты"]
    set_last_digits = set(last_digits.tolist())
    list_last_digits = list(set_last_digits)

    list_number = []
    list_summa_spent = []
    list_cashback = []
    for num in list_last_digits:
        if pd.notna(num):
            spent = data.loc[data["Номер карты"] == num]
            summa_spent = sum(spent["Сумма операции с округлением"])
            list_summa_spent.append(summa_spent)
            cashback = round(summa_spent / 100, 2)
            list_cashback.append(cashback)
            number = ""
            for symbol in str(num):
                if symbol.isdigit() and pd.notna(symbol):
                    number += symbol
            list_number.append(number)
    # Используем zip для объединения элементов по индексам
    combined = zip(list_number, list_summa_spent, list_cashback)

    # Создаем список словарей
    list_of_dicts = [
        {"last_digits": item1, "total_spent": item2, "cashback": item3} for item1, item2, item3 in combined
    ]

    return list_of_dicts


def get_top_five_max_prices(data: DataFrame) -> list:
    """Выводит список словарей топ-5 транзакций"""
    # сортируем df
    sort_data = data.sort_values("Сумма операции").head(5)

    list_date = sort_data["Дата платежа"].tolist()
    list_amount = sort_data["Сумма операции"].tolist()
    list_category = sort_data["Категория"].tolist()
    list_description = sort_data["Описание"].tolist()

    # Используем zip для объединения элементов по индексам
    combined = zip(list_date, list_amount, list_category, list_description)
    # Создаем список словарей
    list_of_dicts = [
        {"date": item1, "amount": item2, "category": item3, "description": item4}
        for item1, item2, item3, item4 in combined
    ]
    return list_of_dicts


def get_user_settings(path: str) -> dict:
    """Выводит словарь со списками валют и акций"""
    with open(path) as f:
        data = json.load(f)
    return data


"""Курс валют. Стоимость акций из S&P500."""
load_dotenv()

API_KEY = os.getenv("API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data/latest"


def conversion_currency(currency: list) -> list:
    """Выводит список словарей с курсами валют"""
    # Запрос к API
    result_currency = []
    for cur in currency:
        response = requests.get(
            BASE_URL, params={"base": cur, "symbols": "RUB"}, headers={"apikey": API_KEY}, timeout=30
        )
        response.raise_for_status()

        data = response.json()
        result = {"currency": data["base"], "rate": data["rates"]["RUB"]}
        result_currency.append(result)
    return result_currency


API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")
BASE_URL_STOCKS = "https://api.twelvedata.com/price"


def conversion_stocks(prices_stocks: list) -> list:
    """Выводит список словарей с курсами валют"""
    # Инициализация с помощью API-ключа
    td = TDClient(apikey=API_KEY_STOCKS)

    result_stocks = []
    for stock in prices_stocks:
        data = td.price(symbol=stock).as_json()

        result = {"stock": stock, "price": data["price"]}
        result_stocks.append(result)
    return result_stocks


if __name__ == "__main__":
    file_path = r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx"
    all_transactions = read_date_as_df(file_path)
    stock_path = r"C:\Training\Python-development\Project\Sky_Pro_Project3\user_settings.json"
    stock_currencies = get_user_settings(stock_path)
    stocks = stock_currencies["user_stocks"]  # ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    currencies = stock_currencies["user_currencies"]  # ['USD', 'EUR']
    # print(get_greetings())
    # print(read_date_as_df(r'C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx'))
    # print(get_card_info(all_transactions))
    # print(get_top_five_max_prices(all_transactions))
    # print(get_user_settings(stock_path))
    print(conversion_stocks(stocks))
