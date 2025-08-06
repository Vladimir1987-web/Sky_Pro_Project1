import json
import logging

import pandas as pd

from src.utils import read_date_as_df

# Основная конфигурация logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=r"C:\Training\Python-development\Project\Sky_Pro_Project3\logs\services.log",
    encoding="utf-8",  # Запись логов в файл
    filemode="w",
)

app_logger = logging.getLogger(__name__)


def get_simple_search(transactions: list, keyword: str) -> str:
    """Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""
    app_logger.info("Фильтрация транзакций по строке поиска")
    list_transactions = []
    for transaction in transactions:
        transaction["Дата операции"] = pd.to_datetime(transaction["Дата операции"]).strftime("%Y-%m-%d")
        if isinstance(transaction["Категория"], str) and keyword in transaction["Категория"]:
            list_transactions.append(transaction)
        elif isinstance(transaction["Описание"], str) and keyword in transaction["Описание"]:
            list_transactions.append(transaction)
    app_logger.info("Вывод информации в формате json")
    return json.dumps(list_transactions, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    all_transactions = read_date_as_df(r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx")
    transactions_for_service = all_transactions.to_dict("records")
    print(transactions_for_service)
    print(get_simple_search(transactions_for_service, "Линзомат"))
