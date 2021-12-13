from typing import Mapping, Tuple
from time import sleep
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from modules.scraping.searcher.utils import get_original, make_float, remove_chars
from modules.cereal import Cereal, Nutrition
from modules.scraping.searcher.browser import get_browser


def __get_links(list):
    links = []
    for elem in list:
        ref = elem.get_attribute("href")
        links.append("https://www.nemlig.com/" + ref)
    else:
        pass
    return links


def get_nemlig_page(search_name: str, brand: str):
    browser = get_browser("https://www.nemlig.com/")

    # click on cookie accept
    elem = browser.find_element_by_xpath('//*[@id="coiPage-1"]/div[2]/div[1]/button[3]')
    if elem.is_displayed():
        elem.click()  # this will click the element if it is there

    sleep(3)

    # Find search field
    elem = browser.find_element_by_xpath('//*[@id="site-header-search-field-main"]')
    elem.send_keys(search_name)
    elem.submit()

    sleep(3)

    Result_set = browser.find_elements_by_class_name("productlist-item__link")
    links = __get_links(Result_set)

    browser.close()

    links_with_name_and_brand = map(lambda link: (link, search_name, brand), links)

    threads = min(len(links), 3)
    with ThreadPoolExecutor(threads) as ex:
        return list(ex.map(__get_single_cereal, links_with_name_and_brand))


def __get_single_cereal(params: Tuple[str, str, str]) -> Cereal:
    link, search_name, the_brand = params

    browser = get_browser(link)
    sleep(3)

    navn = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/h1'
    ).get_attribute("innerText")
    maerke = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/accordion/div[2]/content/div[1]/span[2]'
    ).get_attribute("innerText")
    pris = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/div[3]/div[1]/pricecontainer-unitprice/div/span[2]'
    ).get_attribute("innerHTML")
    gram = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/h2'
    ).get_attribute("innerHTML")

    nutritions = __get_nutritions(browser)

    fat = make_float(nutritions.get("Fedt").replace("g", ""))
    carbohydrates = make_float(nutritions.get("Kulhydrat").replace("g", ""))
    protein = make_float(nutritions.get("Protein").replace("g", ""))
    salt = make_float(nutritions.get("Salt").replace("g", ""))

    fiber = nutritions.get("Kostfibre")
    if fiber:
        fiber = make_float(nutritions.get("Kostfibre").replace("g", ""))
    else:
        fiber = 0

    calories = make_float(nutritions.get("Energi").split("/")[1].replace("kcal", ""))

    browser.close()

    name = navn
    brand = maerke
    price = make_float(pris)
    gram = float(gram.split(" ")[0])

    is_original = search_name + the_brand == name + brand

    return Cereal(
        name,
        brand,
        {"nemlig": price},
        gram,
        is_original,
        Nutrition(
            protein=protein,
            salt=salt,
            carbohydrates=carbohydrates,
            fat=fat,
            fiber=fiber,
            calories=calories
        ),
    )


def __get_nutritions(browser):
    tbody = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[1]/div/product-detail-declaration/div[1]/table/tbody'
    ).get_attribute("innerHTML")
    html = etree.HTML(tbody)

    items = {}

    # key = None - Protein
    # if key == None -> key = Protein
    # key is not None -> {key: value}
    # key = None

    for tr in html.iter("tr"):
        tds = tr.findall("td")
        key = None
        for td in tds:
            for item in td.itertext():
                value = item.replace(" ", "").replace("\n", "")
                if value:
                    if key is None:
                        key = value
                    else:
                        items.setdefault(key, value)
                        key = None

    return items


if __name__ == "__main__":
    cereals = get_nemlig_page("Cornflakes", "Kellogg's")
    for cereal in cereals:
        print(cereal)
