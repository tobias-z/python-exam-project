from typing import Mapping
from time import sleep
from browser import get_browser


def get_nemlig_page(search_name: str):
    browser = get_browser("https://www.nemlig.com/")

    # click on cookie accept
    elem = browser.find_element_by_xpath('//*[@id="coiPage-1"]/div[2]/div[1]/button[3]')
    elem.click()

    sleep(3)

    # Find search field
    elem = browser.find_element_by_xpath('//*[@id="site-header-search-field-main"]')
    elem.send_keys(search_name)
    elem.submit()

    sleep(3)
    return browser.page_source
