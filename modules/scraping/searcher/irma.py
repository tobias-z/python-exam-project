from time import sleep
from typing import Dict, List
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from lxml import etree

from exam_project.modules.scraping.cereal import Cereal, Nutrition
from exam_project.modules.scraping.searcher.browser import get_browser
from exam_project.modules.scraping.searcher.utils import make_float, remove_chars


def get_irma_page(search_name: str) -> List[Cereal]:
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

    browser.close()
    threads = min(len(links), 6)
    with ThreadPoolExecutor(threads) as ex:
        return list(ex.map(__get_single_page, links))


def __get_single_page(link: str) -> Cereal:
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
        html, "Protein", "Salt", "Kulhydrater", "Fedt", "Kostfibre"
    )

    browser.close()
    return Cereal(
        name,
        brand,
        price,
        grams,
        Nutrition(
            protein=nutritions.get("Protein"),
            salt=nutritions.get("Salt"),
            carbohydrates=nutritions.get("Kulhydrater"),
            fat=nutritions.get("Fedt"),
            fiber=nutritions.get("Kostfibre"),
        ),
    )


def __get_nutritions(html, *names: str):
    nutitions: Dict[str, float] = {}
    for item in html.iter("div"):
        for name in names:
            if name in item.text:
                nutitions.setdefault(
                    name, make_float(remove_chars(item.find("span").text))
                )
    return nutitions


if __name__ == "__main__":
    cereal = __get_single_page(
        "https://mad.coop.dk/kolonial/morgenmad-og-mellemmaltid/cornflakes/kelloggs-kelloggs-cornflakes-p-5738001092490"
    )
    print(
        cereal.name,
        cereal.brand,
        cereal.grams,
        cereal.price,
        cereal.nutrition.fat,
        cereal.nutrition.protein,
        cereal.nutrition.carbohydrates,
        cereal.nutrition.fiber,
        cereal.nutrition.salt,
    )
