import re
import time
from typing import Dict, List, Tuple, Union

from bs4 import BeautifulSoup
from bs4.element import ResultSet
from models import Product
from requests import Session
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver import create_webdriver

from .constants import BASE_URL, RELATIVE_URL

absolute_url = BASE_URL + RELATIVE_URL


def create_soup(url: str) -> BeautifulSoup:
    session = Session()
    responce = session.get(url)
    html_content = responce.text

    return BeautifulSoup(html_content, "lxml")


def open_page_with_selenium(url: str, driver: Chrome) -> BeautifulSoup:

    driver.get(url)

    accordion_button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.cmp-accordion__button"))
    )
    accordion_button.click()

    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, "lxml")

    return soup


def get_products_links(soup: BeautifulSoup) -> List[str]:
    all_products_links: List[str] = []
    products_for_parsing: ResultSet = (
        soup.find("div", class_="product-category")
        .find("ul", class_="cmp-category__row")
        .find_all("li", class_="cmp-category__item")
    )

    for product in products_for_parsing:
        link = product.find("a")["href"]
        all_products_links.append(link)

    return all_products_links


def parse_product_info(soup: BeautifulSoup) -> Tuple[str, str]:

    container_product = soup.find(
        "main", class_="container responsivegrid pt-responsive"
    )
    name: str = container_product.find(
        "span", class_="cmp-product-details-main__heading-title"
    ).text.replace("®", "")
    description: str = container_product.find("div", class_="cmp-text").text.strip()

    return name, description


def parse_nutrients_info(
    nutrients_elements: ResultSet,
) -> Dict[str, dict[str, Union[dict, str]]]:

    pattern = r"\d+\.?\d*"
    nutrients_name: list = ["colories", "fats", "carbs", "proteins"]
    nutrients_data: Dict[str, dict[str, Union[dict, str]]] = {}

    for element, nutrient in zip(nutrients_elements, nutrients_name):
        content = (
            element.find("span", class_="value")
            .find("span", attrs={"aria-hidden": "true"})
            .text.strip()
        )

        amount, unit, metric = "N/A", "N/A", "N/A"

        try:
            amount = re.search(pattern, content).group()
            unit = str(content.split("/")[1])
            metric = (
                element.find("span", class_="metric")
                .find("span", attrs={"aria-hidden": "true"})
                .text.strip()
                .replace("\n                    ", " ")
            )
        except (ValueError, AttributeError, IndexError) as e:
            print(f"An error occurred while parsing {nutrient}: {e}")

        nutrients_data[nutrient] = {
            "value": {"amount": amount, "unit": unit},
            "metric": metric,
        }

    return nutrients_data


def parse_additional_nutriens_info(
    nutrients_details: ResultSet,
) -> Dict[str, dict[str, Union[dict, str]]]:
    pattern = r"(\d+(\.\d+)?)\s*(г|мл)"

    nutrients_details_name: list = ["unsaturated_fats", "sugar", "salt", "portion"]
    nutrients_details_data: Dict[str, dict[str, Union[dict, str]]] = {}

    for detail, nutrient_detail in zip(nutrients_details, nutrients_details_name):
        content = detail.find("span", attrs={"aria-hidden": "true"}).text.strip()

        (
            amount,
            unit,
        ) = (
            "N/A",
            "N/A",
        )

        try:
            amount = re.search(pattern, content).group(1)
            unit = re.search(pattern, content).group(3)

        except (ValueError, AttributeError, IndexError) as e:
            print(f"An error occurred while parsing {nutrient_detail}: {e}")

        nutrients_details_data[nutrient_detail] = {
            "value": {"amount": amount, "unit": unit},
        }

    return nutrients_details_data


def parser_data(url: str) -> List[Product]:
    result: List[Product] = []
    soup = create_soup(url=url)

    product_links: List[str] = get_products_links(soup)

    driver: Chrome = create_webdriver()

    for product_link in product_links[:2]:
        absolute_product_link: str = BASE_URL + product_link
        soup: BeautifulSoup = open_page_with_selenium(
            url=absolute_product_link, driver=driver
        )

        name, description = parse_product_info(soup)

        nutrients_elements: ResultSet = soup.find_all(
            "li", class_="cmp-nutrition-summary__heading-primary-item"
        )
        nutrients_data: Dict = parse_nutrients_info(nutrients_elements)

        nutrients_details = soup.find(
            "div", class_="cmp-nutrition-summary__details-column-view-desktop"
        ).find_all("li")
        nutrients_details_data: Dict = parse_additional_nutriens_info(nutrients_details)

        product = Product(
            name=name,
            description=description,
            **nutrients_data,
            **nutrients_details_data,
        )
        print(product.name)
        result.append(product)
    print(
        f'{len(result)} products have been saved into the JSON file, which is "products" '
    )
    driver.quit()

    return result
