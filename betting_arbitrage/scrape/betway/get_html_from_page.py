import time
from random import random
from selenium.webdriver.common.by import By
from scrape.shared import get_chrome

TABLE_SELECTOR = "div.layout.subcategoryLayout.collection.vertical"
COLLAPSED_HEADER_SELECTOR = '.collapsableHeader[collapsed="true"]'


def get_html_from_page(url):
    chrome = get_chrome()
    chrome.get(url)
    expand_all(chrome)
    body = chrome.find_element(By.TAG_NAME, "body")
    return body.get_attribute("innerHTML")


def expand_all(chrome):
    headers_to_click = get_headers_to_click(chrome)
    while len(headers_to_click) > 0:
        for tag in headers_to_click:
            try:
                tag.click()
            except:
                continue
            time.sleep(1 + random())
        headers_to_click = get_headers_to_click(chrome)


def get_headers_to_click(browser):
    return browser.find_elements(
        By.CSS_SELECTOR, f"{TABLE_SELECTOR} {COLLAPSED_HEADER_SELECTOR}"
    )


if __name__ == "__main__":
    print(get_html_from_page(url="https://betway.com/en/sports/sct/esports/cs-go"))
