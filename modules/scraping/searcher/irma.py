from time import sleep
from typing import Dict, List, Tuple
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from lxml import etree

from modules.cereal import Cereal, Nutrition
from modules.scraping.searcher.browser import get_browser
from modules.scraping.searcher.utils import get_original, make_float, remove_chars


def get_irma_page(search_name: str, brand: str) -> List[Cereal]:
    browser = get_browser("https://mad.coop.dk/irma")

    # Find search field
    elem = browser.find_element_by_xpath('//*[@id="site_header_search_id"]')
    elem.send_keys(search_name)
    elem.submit()

    sleep(3)

    links = list(
        map(
            lambda l: l.get_attribute("href"),
            browser.find_element_by_xpath(
                '//*[@id="app"]/div[4]/header/div[4]/div/div/div[2]/div/div[2]/div[3]/div/div[2]/div'
            ).find_elements_by_class_name("c-product-tile__title"),
        )
    )

    links_with_name_and_brand = map(lambda link: (link, search_name, brand), links)

    browser.close()
    threads = min(len(links), 3)
    with ThreadPoolExecutor(threads) as ex:
        return list(ex.map(__get_single_page, links_with_name_and_brand))


def __get_single_page(params: Tuple[str, str, str]) -> Cereal:
    link, search_name, the_brand = params

    browser = get_browser(link)
    sleep(3)

    soup = BeautifulSoup(browser.page_source, "html.parser")

    name = soup.find("h1", class_="c-product-detail__title").text
    brand = soup.find("p", class_="text-15 mb-5").text
    price = make_float(
        soup.find("div", class_="text-grey-darker mb-10 md:mb-0")
        .text.replace("kr. pr. kg", "")
        .replace(" ", "")
        .replace("-", "")
    )
    grams = (
        make_float(soup.find("div", class_="mt-5 mb-5").text.replace(" kg", ""))
    ) * 1000

    outer_div = browser.find_element_by_xpath(
        '//*[@id="ingredienser"]/div[2]/div'
    ).get_attribute("innerHTML")
    html = etree.HTML(outer_div)

    nutritions = __get_nutritions(
        html, "Protein", "Salt", "Kulhydrater", "Fedt", "Kostfibre", "Energi"
    )
    calories = make_float(nutritions.get("Energi").split("/")[1].replace("kcal", ""))

    is_original = search_name + the_brand == name + brand

    browser.close()
    return Cereal(
        name,
        brand,
        {"irma": price},
        grams,
        is_original,
        Nutrition(
            protein=nutritions.get("Protein"),
            salt=nutritions.get("Salt"),
            carbohydrates=nutritions.get("Kulhydrater"),
            fat=nutritions.get("Fedt"),
            fiber=nutritions.get("Kostfibre"),
            calories=calories,
        ),
    )


def __get_nutritions(html, *names: str):
    nutitions: Dict[str, float] = {}
    for item in html.iter("div"):
        for name in names:
            if name in item.text:
                value = item.find("span").text
                if name != "Energi":
                    value = make_float(remove_chars(value))
                nutitions.setdefault(name, value)
    return nutitions


if __name__ == "__main__":
    cereals = get_irma_page("Cornflakes", "something")
    for cereal in cereals:
        print(
            cereal.brand,
            cereal.name,
            cereal.grams,
            cereal.price,
            cereal.nutrition.fat,
            cereal.nutrition.protein,
            cereal.nutrition.carbohydrates,
            cereal.nutrition.fiber,
            cereal.nutrition.salt,
            cereal.nutrition.calories,
        )
