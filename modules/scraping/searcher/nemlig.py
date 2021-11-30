from typing import Mapping
from time import sleep
from browser import get_browser


def get_irma_page(search_name: str):
    browser = get_browser("https://www.nemlig.com/")

    # Find search field
    elem = browser.find_element_by_xpath(
        '//*[@id="site-header-search-field-main"]'
    )
    elem.send_keys(search_name)
    elem.submit()

    sleep(3)

    return browser.page_source


if __name__ == "__main__":
    print(get_irma_page("Cornflakes"))