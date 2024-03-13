import json
from dataclasses import asdict
from pathlib import Path

# from constants import PRODUCTS_FILE
from models import Product


def save_to_json(data: list[Product], filename: Path):

    with open(f"{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, default=asdict, ensure_ascii=False, indent=4)


# def load_from_json(filename: Path):

#     with open(f"{filename}", "r") as f:
#         products = json.load(f)


# json_data = load_from_json(filename=PRODUCTS_FILE)

# print(json_data)
