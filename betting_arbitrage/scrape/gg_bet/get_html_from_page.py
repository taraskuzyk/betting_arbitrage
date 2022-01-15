import time
from random import random

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

from scrape.betway.css_strings import TABLE_SELECTOR, COLLAPSED_HEADER_SELECTOR
from scrape.shared import get_chrome


def get_html_from_page(url):
    chrome = get_chrome()
    chrome.get(url)
    time.sleep(3)
    while "One more step" in get_body_html(chrome):
        time.sleep(1)
    time.sleep(3)
    expand_all(chrome)
    return get_body_html(chrome)


def get_body_html(chrome):
    body = chrome.find_element(By.TAG_NAME, "body")
    return body.get_attribute("innerHTML")


def expand_all(chrome: webdriver.Chrome):
    body = chrome.find_element(By.TAG_NAME, "body")
    # TODO: only loads first page - try to figure out a way to load all pages
    for _ in range(30):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(5+random())


def get_headers_to_click(browser):
    return browser.find_elements(
        By.CSS_SELECTOR, f"{TABLE_SELECTOR} {COLLAPSED_HEADER_SELECTOR}"
    )


if __name__ == "__main__":
    print(get_html_from_page(url="https://gg.bet/en/counter-strike/"))
