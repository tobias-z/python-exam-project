from time import sleep
from typing import List
from browser import get_browser
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from lxml import etree


from exam_project.modules.scraping.cereal import Cereal, Nutrition
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
                '//*[@id="app"]/div[5]/header/div[4]/div/div/div[3]/div/div[2]/div[3]/div/div[2]/div'
            ).find_elements_by_class_name("c-product-tile__title"),
        )
    )

    browser.close()
    with ThreadPoolExecutor(len(links)) as ex:
        return list(ex.map(__get_single_page, links))


def __get_single_page(link: str) -> Cereal:
    browser = get_browser(link)
    sleep(3)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    dom = etree.HTML(str(soup))

    name = dom.xpath(
        '//*[@id="app"]/div[5]/div[1]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/h1'
    )[0].text
    brand = dom.xpath(
        '//*[@id="app"]/div[5]/div[1]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/div[1]/p'
    )[0].text
    price = make_float(
        dom.xpath(
            '//*[@id="app"]/div[5]/div[1]/div[2]/div/div/div/div[1]/div[1]/div/div[2]/div/div[3]/div/div[2]'
        )[0]
        .text.replace("kr. pr. kg", "")
        .replace(" ", "")
        .replace("-", "")
    )
    grams = (
        make_float(
            dom.xpath(
                '//*[@id="app"]/div[5]/div[1]/div[2]/div/div/div/div/div[1]/div/div[2]/div/div[1]/div[2]/div/text()'
            )[0].replace(" kg", "")
        )
        * 1000
    )

    outer_div = dom.xpath('//*[@id="ingredienser"]/div[2]/div')[0]
    html = etree.HTML(etree.tostring(outer_div, pretty_print=True))

    browser.close()
    return Cereal(
        name,
        brand,
        price,
        grams,
        Nutrition(
            protein=__get_nutrition(html, "Protein"),
            salt=__get_nutrition(html, "Salt"),
            carbohydrates=__get_nutrition(html, "Kulhydrater"),
            fat=__get_nutrition(html, "Fedt"),
            fiber=__get_nutrition(html, "Kostfibre"),
        ),
    )


def __get_nutrition(html, name: str):
    for item in html.iter("div"):
        if name in item.text:
            return make_float(remove_chars(item.find("span").text))


if __name__ == "__main__":
    cereals = get_irma_page("müsli")
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
