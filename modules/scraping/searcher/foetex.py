from time import sleep
from typing import List

from browser import get_browser
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from lxml import etree

from exam_project.modules.scraping.cereal import Cereal, Nutrition
from exam_project.modules.scraping.searcher.utils import make_float, remove_chars

ROOT_URL = "https://hjem.foetex.dk"


def get_foetex_page(search_name: str) -> List[Cereal]:
    browser = get_browser(ROOT_URL)

    # click on cookie accept
    elem = browser.find_element_by_xpath('//*[@id="coiPage-1"]/div[2]/div[1]/button[3]')
    elem.click()

    sleep(3)

    # Find search field
    elem = browser.find_element_by_xpath(
        '//*[@id="__next"]/div[1]/header/div[2]/div/div[2]/div[2]/form/div/div/input'
    )
    elem.send_keys(search_name)
    elem.submit()

    sleep(3)

    links = __get_links(browser.page_source)

    browser.close()

    with ThreadPoolExecutor(len(links)) as ex:
        return list(filter(None, ex.map(__get_single_cereal, links)))


def __get_links(page_source) -> List[str]:
    soup = BeautifulSoup(page_source, "html.parser")
    tags = soup.find_all("a", href=True)
    links: List[str] = []
    for a in tags:
        url = a["href"]
        if "/produkt" in url:
            links.append(ROOT_URL + url)
    return links


def __get_single_cereal(link: str) -> Cereal:
    browser = __get_correct_browser_state(link)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    dom = etree.HTML(str(soup))
    browser.close()

    name = dom.xpath(
        '//*[@id="__next"]/div[1]/main/div[1]/div[1]/section[2]/article/div[3]/span'
    )[0].text
    brand = dom.xpath(
        '//*[@id="__next"]/div[1]/main/div[1]/div[1]/section[2]/article/div[4]/span/strong'
    )[0].text
    price = make_float(
        dom.xpath(
            '//*[@id="__next"]/div[1]/main/div[1]/div[1]/section[2]/div[1]/div[1]/div[2]/div/span/text()[4]'
        )[0]
    )
    grams = make_float(
        dom.xpath(
            '//*[@id="__next"]/div[1]/main/div[1]/div[1]/section[2]/article/div[4]/span/text()[2]'
        )[0]
    )

    tbody = dom.xpath(
        '//*[@id="__next"]/div[1]/main/div[1]/div[1]/section[2]/div[2]/section[2]/div/div/div/table/tbody'
    )
    if len(tbody) == 0:
        # Cannot fine Cornflakes Salling tbody for some reason
        return None

    html = etree.HTML(etree.tostring(tbody[0], pretty_print=True))
    fat = __get_nutrition(html, "Fedt")
    protein = __get_nutrition(html, "Protein")
    carbohydrates = __get_nutrition(html, "Kulhydrater")
    fiber = __get_nutrition(html, "Kostfibre")
    salt = __get_nutrition(html, "Salt")

    return Cereal(
        name,
        brand,
        price,
        grams,
        Nutrition(protein, carbohydrates, fiber, fat, salt),
    )


def __get_correct_browser_state(link: str):
    browser = get_browser(link)
    browser.find_element_by_xpath(
        '//*[@id="coiPage-1"]/div[2]/div[1]/button[3]'
    ).click()
    sleep(2)
    browser.find_element_by_xpath(
        '//*[@id="__next"]/div[1]/main/div[1]/div[1]/section[2]/div[2]/section[2]/button'
    ).click()

    sleep(3)
    return browser


def __get_nutrition(tbody_html, name: str):
    items = []
    stop = False
    for item in tbody_html.iter("span"):
        text = item.text
        items.append(text)
        if stop:
            break

        if text == name:
            stop = True

    return make_float(remove_chars(items[-1]))


if __name__ == "__main__":
    cereals = get_foetex_page("muesli")
    for cereal in cereals:
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
