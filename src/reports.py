from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd

from src.utils import read_date_as_df


# Декоратор с параметрами
def report_to_file(filename):
    def inner(spending_by_category):
        @wraps(spending_by_category)
        def wrapper(*args, **kwargs):
            result = spending_by_category(*args, **kwargs)
            with open(filename, "w", encoding="utf-8") as f:
                result.to_json(f, orient="records", indent=4, force_ascii=False)

            return result

        return wrapper

    return inner


@report_to_file("fast_food_report.json")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)."""
    global date_dt
    if date:
        date_dt = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    elif not date:
        date_dt = datetime.now()
        print(date_dt)
    start_dt = date_dt - pd.DateOffset(month=3)
    selected_transactions = transactions[
        (pd.to_datetime(transactions["Дата операции"]) >= start_dt)
        & (pd.to_datetime(transactions["Дата операции"]) <= date_dt)
        & (transactions["Категория"] == category)
        & (transactions["Сумма операции"] < 0)
    ]
    return selected_transactions


if __name__ == "__main__":
    all_transactions = read_date_as_df(r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx")
    print(spending_by_category(all_transactions, "Фастфуд""2018-07-25 20:10:33"))
