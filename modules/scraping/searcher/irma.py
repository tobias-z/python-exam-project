from typing import Mapping
from time import sleep
from browser import get_browser


def get_irma_page(search_name: str):
    browser = get_browser("https://mad.coop.dk/irma")

    # Find search field
    elem = browser.find_element_by_xpath('//*[@id="site_header_search_id"]')
    elem.send_keys(search_name)
    elem.submit()

    sleep(3)
    print(browser.page_source)

    return browser.page_source
