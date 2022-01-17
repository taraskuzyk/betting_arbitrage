import time
from random import random
from selenium.webdriver.common.by import By

from scrape.betway.css_strings import TABLE_SELECTOR, COLLAPSED_HEADER_SELECTOR
from scrape.shared import get_chrome


def get_html_from_page(url):
    chrome = get_chrome()
    chrome.get(url)
    time.sleep(3)
    expand_all(chrome)
    body = chrome.find_element(By.TAG_NAME, "body")
    return body.get_attribute("innerHTML")


def expand_all(chrome):
    headers_to_click = get_headers_to_click(chrome)
    count = 0
    while len(headers_to_click) > 0 and count < 25:
        count += 1  # prevent weird stuck bug
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
