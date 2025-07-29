from src.services import get_simple_search
from src.utils import read_date_as_df
from src.views import get_main_page_info


def maim():
    main_page_result = get_main_page_info("2021-07-25 20:10:33")
    print(main_page_result)

    all_transactions = read_date_as_df(r"C:\Training\Python-development\Project\Sky_Pro_Project3\data\operations.xlsx")
    transactions_for_service = all_transactions.to_dict("records")
    service_result = get_simple_search(transactions_for_service, "Константин Л.")
    print(service_result)


if __name__ == "__main__":
    maim()
