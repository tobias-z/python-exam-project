from typing import Mapping
from time import sleep
import requests
from bs4 import BeautifulSoup

from modules.scraping.searcher.browser import get_browser


def get_nemlig_page(search_name: str):
    browser = get_browser("https://www.nemlig.com/")

    # click on cookie accept
    # browser.find_element_by_xpath('//*[@id="coiPage-1"]/div[2]/div[1]/button[3]'):
    #    elem = browser.find_element_by_xpath('//*[@id="coiPage-1"]/div[2]/div[1]/button[3]')
    #
    #     elem.click()

    sleep(3)

    # Find search field
    elem = browser.find_element_by_xpath('//*[@id="site-header-search-field-main"]')
    elem.send_keys(search_name)
    elem.submit()

    Result_set = browser.find_elements_by_class_name("productlist-item_link")
    # browser.find_elements_by_xpath("//a[@class='productlist-item__link'][@href]")

    Attribute_set = [link.text for link in Result_set]
    source = browser.current_url

    sleep(3)
    return Result_set, source, Attribute_set


if __name__ == "__main__":
    Result_set, source, Attribute_set = get_nemlig_page("Cornflakes")
    print(source)
    print(Result_set)
    # print(Attribute_set)
    # links, number = links(Result_set)
    # print(number)
    # print(links)

    # print(f'There are {len(Result_set)}')
    # print(Result_set)

    # links, number = get_product_links(Result_set)


def links(list):
    links = []
    for elem in list:
        my_href = elem.get_attribute("href")
        if "productlist-item" in my_href:
            ref = my_href
            links.append(ref)
        else:
            pass
    return links


def get_product_links(list):
    links = []
    counter = 0
    for link in list:
        r = requests.get(link)
        r.raise_for_status()
        soup = bs4.BeautifulSoup(r.text, "html.parser")
        elems = soup.select("a")
        number = len(elems)
        counter += 1
        links.append(r)
    return links, number
