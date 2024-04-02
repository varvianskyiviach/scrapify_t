import json
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List

from .constants import PRODUCTS_FILE
from .models import Product


def save_to_json(data: list[Product], filename: Path):

    with open(f"{filename}", "w", encoding="utf-8") as f:
        json.dump(data, f, default=asdict, ensure_ascii=False, indent=4)


def load_from_json(filename: Path) -> List[Dict]:

    with open(f"{filename}", "r") as f:
        return json.load(f)


def get_all_products() -> List[Dict]:
    json_data = load_from_json(filename=PRODUCTS_FILE)

    all_products: List[Product] = [Product(**instance) for instance in json_data]

    return [asdict(product) for product in all_products]


def get_product(product_name: str) -> Dict | None:
    json_data = load_from_json(filename=PRODUCTS_FILE)

    for instance in json_data:
        if instance["name"] == product_name:
            product: Product = Product(**instance)

            return asdict(product)
    return None


def get_product_for_detail(product_name: str, product_field: str) -> Dict[str, str] | None:
    product: Product = get_product(product_name)

    result: Dict = {}
    if product:
        result["name"] = product.get("name")
        try:
            result[product_field] = product.get(product_field)
        except AttributeError:
            result[product_field] = None

        return result
    return None
