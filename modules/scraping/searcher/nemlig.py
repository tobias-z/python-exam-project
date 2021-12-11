from typing import Mapping
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from modules.scraping.searcher.utils import make_float, remove_chars
from modules.scraping.cereal import Cereal, Nutrition
from modules.scraping.searcher.browser import get_browser


def __get_links(list):
    links = []
    for elem in list:
        ref = elem.get_attribute("href")
        links.append("https://www.nemlig.com/" + ref)
    else:
        pass
    return links


def get_nemlig_page(search_name: str):
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

    threads = min(len(links), 6)
    with ThreadPoolExecutor(threads) as ex:
        return list(ex.map(__get_single_cereal, links))


def __get_single_cereal(link: str) -> Cereal:

    browser = get_browser(link)

    sleep(3)

    navn = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/accordion/div[2]/content/div[4]/span[2]'
    ).get_attribute("innerText")
    maerke = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/accordion/div[2]/content/div[1]/span[2]'
    ).get_attribute("innerText")
    pris1 = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/div[3]/div[1]/pricecontainer/div/div[2]/span'
    ).get_attribute("innerHTML")
    pris2 = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/div[3]/div[1]/pricecontainer/div/div[2]/sup'
    ).get_attribute("innerHTML")
    gram = browser.find_element_by_xpath(
        '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[2]/h2'
    ).get_attribute("innerHTML")

    fedt = (
        browser.find_element_by_xpath(
            '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[1]/div/product-detail-declaration/div[1]/table/tbody/tr[3]/td[2][text()]'
        )
        .get_attribute("innerText")
        .split("''")
    )
    kulhydrat = (
        browser.find_element_by_xpath(
            '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[1]/div/product-detail-declaration/div[1]/table/tbody/tr[5]/td[2][text()]'
        )
        .get_attribute("innerText")
        .split("''")
    )
    protein = (
        browser.find_element_by_xpath(
            '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[1]/div/product-detail-declaration/div[1]/table/tbody/tr[8]/td[2][text()]'
        )
        .get_attribute("innerText")
        .split("''")
    )
    salt = (
        browser.find_element_by_xpath(
            '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[1]/div/product-detail-declaration/div[1]/table/tbody/tr[9]/td[2][text()]'
        )
        .get_attribute("innerText")
        .split("''")
    )
    fiber = (
        browser.find_element_by_xpath(
            '//*[@id="page-content"]/div/productdetailpage/section/div[1]/render-partial/div/product-detail/accordion-group/div/div/div[1]/div/product-detail-declaration/div[1]/table/tbody/tr[7]/td[2][text()]'
        )
        .get_attribute("innerText")
        .split("''")
    )

    browser.close()

    name = navn
    brand = maerke
    price = float(pris1 + "." + pris2)
    gram = float(gram.replace(" g / Kellogg's", ""))

    fat = make_float(remove_chars(fedt[0]))
    carbohydrates = make_float(remove_chars(kulhydrat[0]))
    protein = make_float(remove_chars(protein[0]))
    salt = make_float(remove_chars(salt[0]))
    fiber = make_float(remove_chars(fiber[0]))

    return Cereal(
        name, brand, price, gram, Nutrition(protein, salt, carbohydrates, fat, fiber)
    )


if __name__ == "__main__":
    cereal = get_nemlig_page("Cornflakes")
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
