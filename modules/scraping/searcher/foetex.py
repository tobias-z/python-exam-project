from time import sleep
from browser import get_browser
from bs4 import BeautifulSoup


def get_foetex_page(search_name: str):
    browser = get_browser("https://hjem.foetex.dk/")

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

    return browser.page_source


if __name__ == "__main__":
    name = "Cornflakes".lower()
    soup = BeautifulSoup(get_foetex_page(name), "html.parser")
    tags = soup.find_all("div > div > a", href=True)
    for a in tags:
        url = a["href"]
        if name and "/produkt" in url:
            print("url: ", url)
