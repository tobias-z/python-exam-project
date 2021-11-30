from typing import Mapping
from time import sleep
from browser import get_browser


def get_foetex_page(search_name: str):
    browser = get_browser("https://hjem.foetex.dk/")

    # Find search field
    elem = browser.find_element_by_xpath(
        '//*[@id="__next"]/div[1]/header/div[2]/div/div[2]/div[2]/form/div/div/input'
    )
    elem.send_keys(search_name)
    elem.submit()

    sleep(3)

    return browser.page_source


if __name__ == "__main__":
    print(get_foetex_page("Cornflakes"))
