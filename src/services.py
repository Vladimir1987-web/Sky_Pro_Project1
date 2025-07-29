import json

import pandas as pd

from src.utils import read_date_as_df


def get_simple_search(transactions: list, keyword: str) -> str:
    """Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""
    list_transactions = []
    for transaction in transactions:
        transaction["Дата операции"] = pd.to_datetime(transaction["Дата операции"]).strftime("%Y-%m-%d")
        if isinstance(transaction["Категория"], str) and keyword in transaction["Категория"]:
            list_transactions.append(transaction)
        elif isinstance(transaction["Описание"], str) and keyword in transaction["Описание"]:
            list_transactions.append(transaction)

    return json.dumps(list_transactions, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    all_transactions = read_date_as_df(r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx")
    transactions_for_service = all_transactions.to_dict("records")
    print(get_simple_search(transactions_for_service, "Константин Л."))
