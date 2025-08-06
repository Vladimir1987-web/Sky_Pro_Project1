# Проект Sky_Pro_Project
## Описание:
Это проект служит для анализа транзакций, которые находятся в Excel-файле. Приложение будет генерировать JSON-данные для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.
## Установка:
1. Клонируйте репозиторий:
```git clone https://github.com/Vladimir1987-web/Sky_Pro_Project1```
2. Установите зависимости:
```pip install -r requirements.txt```
## Использование:
Данный проект состоит из пяти модулей:
1. Модуль views.py - принимает на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными:
- Приветствие
- Информация по каждой карте
- Курс валют
- Стоимость акций из S&P500

Пример использования:
```if __name__ == "__main__":
    print(get_main_page_info("2021-07-25 20:10:33"))
```

2. Модуль utils.py -вспомогательный модуль в основном для модуля views.py.
Содержит:
- get_greetings - функцию приветствия пользователя,
- read_date_as_df - функцию, считывающую информацию из excel,
- get_card_info - функцию, выводящую список словарей с информацией по картам,
- get_top_five_max_prices - функцию, выводящую список словарей топ-5 транзакций,
- get_user_settings - функцию, выводящую словарь со списками валют и акций,
- conversion_currency - функцию, выводящую список словарей с курсами валют,
- conversion_stocks - функцию, выводящую список словарей со стоимостью акций.

Пример использования:
```commandline
if __name__ == "__main__":
    file_path = r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx"
    all_transactions = read_date_as_df(file_path)
    stock_path = r"C:\Training\Python-development\Project\Sky_Pro_Project3\user_settings.json"
    stock_currencies = get_user_settings(stock_path)
    stocks = stock_currencies["user_stocks"]  # ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']
    currencies = stock_currencies["user_currencies"]  # ['USD', 'EUR']
    print(get_greetings())
    print(read_date_as_df(r'C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx'))
    print(get_card_info(all_transactions))
    print(get_top_five_max_prices(all_transactions))
    print(get_user_settings(stock_path))
    print(conversion_stocks(stocks))
```

3. Модуль services.py, состоящий из одной функции get_simple_search, в которой пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории.
Пример использования:
```commandline
if __name__ == "__main__":
    all_transactions = read_date_as_df(r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx")
    transactions_for_service = all_transactions.to_dict("records")
    print(get_simple_search(transactions_for_service, "Константин Л."))
```

4. Модуль reports.py, содержащий декоратор report_to_file, который сохраняет результат работы функции spending_by_category в файл, и непосредственно саму функцию spending_by_category, которая возвращает траты по заданной категории за последние три месяца (от переданной даты).

Пример использования:
```commandline
if __name__ == "__main__":
    all_transactions = read_date_as_df(r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx")
    print(spending_by_category(all_transactions, "Фастфуд""2018-07-25 20:10:33"))
```

5. Модуль main.py - главный модуль с функцией main, реализующей работу вех модулей проекта.
Пример использования:
```commandline
if __name__ == "__main__":
    maim()
```

### Тестирование
В пакете tests реализованы четыре модуля для тестирования функций каждого модуля из пакета src:
1) Модуль test_utils.py
2) Модуль test_views.py
3) Модуль test_services.py
4) Модуль test_reports.py