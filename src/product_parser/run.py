from constants import BASE_URL, PRODUCTS_FILE, RELATIVE_URL

from product_parser.parser import parser_data
from product_parser.services import save_to_json


def main():
    absolute_url = BASE_URL + RELATIVE_URL

    data = parser_data(url=absolute_url)
    save_to_json(data, PRODUCTS_FILE)


if __name__ == "__main__":
    main()
