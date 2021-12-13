from time import sleep
from typing import List, Tuple
from typing_extensions import get_origin

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from lxml import etree

from modules.cereal import Cereal, Nutrition
from modules.scraping.searcher.browser import get_browser
from modules.scraping.searcher.utils import get_original, make_float, remove_chars

ROOT_URL = "https://hjem.foetex.dk"


def get_foetex_page(search_name: str, brand: str) -> List[Cereal]:
    browser = get_browser(ROOT_URL)
    __accept_cookies(browser)
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

    links_with_name_and_brand = map(lambda link: (link, search_name, brand), links)

    threads = min(len(links), 3)
    with ThreadPoolExecutor(threads) as ex:
        return list(
            filter(None, ex.map(__get_single_cereal, links_with_name_and_brand))
        )


def __get_links(page_source) -> List[str]:
    soup = BeautifulSoup(page_source, "html.parser")
    tags = soup.find_all("a", href=True)
    links: List[str] = []
    for a in tags:
        url = a["href"]
        if "/produkt" in url:
            links.append(ROOT_URL + url)
    return links


def __get_single_cereal(params: Tuple[str, str, str]) -> Cereal:
    link, search_name, the_brand = params
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

    if brand == "Kellogg's Cornflakes":
        brand = "Kellogg's"

    price = make_float(
        dom.xpath(
            '//*[@id="__next"]/div[1]/main/div[1]/div[1]/section[2]/div[1]/div[1]/div[2]/div/span/text()[4]'
        )[0]
    )
    # price = 1
    grams = make_float(
        dom.xpath(
            '//*[@id="__next"]/div[1]/main/div[1]/div[1]/section[2]/article/div[4]/span/text()[2]'
        )[0]
    )
    # grams = 2

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
    is_original = search_name + the_brand == name + brand

    calories = float(
        __get_nutrition(html, "Energi")
        .split("/")[1]
        .replace("kcal", "")
        .replace(".", "")
    )

    return Cereal(
        name,
        brand,
        {"føtex": price},
        grams,
        is_original,
        Nutrition(protein, carbohydrates, fiber, fat, salt, calories),
    )


def __accept_cookies(browser):
    elem = browser.find_element_by_xpath('//*[@id="coiPage-1"]/div[2]/div[1]/button[3]')
    if elem.is_displayed():
        elem.click()


def __get_correct_browser_state(link: str):
    browser = get_browser(link)
    __accept_cookies(browser)
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

    if name == "Energi":
        return items[-1]

    return make_float(remove_chars(items[-1]))


if __name__ == "__main__":
    cereals = get_foetex_page("Cornflakes", "something")
    for cereal in cereals:
        print(cereal)
