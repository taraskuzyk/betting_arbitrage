import time
from random import random
from selenium.webdriver.common.by import By

from scrape.shared import get_chrome

POWBET_URL = "https://powbet.com/ca/sports"

def get_html_from_page(category, sport):
    chrome = get_chrome()
    chrome.get(POWBET_URL)
    time.sleep(8)
    navigate_to_desired_category(chrome, category, sport)
    expand_all(chrome)
    body = chrome.find_element(By.TAG_NAME, "body")
    return body.get_attribute("innerHTML")


def navigate_to_desired_category(chrome, category, sport):
    category_element = chrome.find_element(By.CSS_SELECTOR, f'[title="{category}"]')
    while category_element is None:
        time.sleep(1)
        category_element = chrome.find_element(By.CSS_SELECTOR, f'[title="{category}"]')
    category_element.click()
    time.sleep(2 * random())
    sport_element_includer = chrome.find_element(
        By.CSS_SELECTOR, f'[title="{sport}"] i'
    )
    sport_element_includer.click()
    time.sleep(2 * random())
    show_all_button = chrome.find_element(
        By.CSS_SELECTOR, '[class*="_asb_redirect-button"]'
    )
    show_all_button.click()
    time.sleep(2 * random())


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
    expansion_panels = browser.find_elements(
        By.CSS_SELECTOR, '.asb-flex-sc[class*="events-tree-table-node"]'
    )
    return [
        panel
        for panel in expansion_panels
        if (panel_has_arrows_down(panel) and panel_doesnt_have_event_arrows_down(panel))
    ]


def panel_doesnt_have_event_arrows_down(panel):
    return (
        len(
            panel.find_elements(By.CSS_SELECTOR, '[class*="row"] [class*="arrow-down"]')
        )
        == 0
    )


def panel_has_arrows_down(panel):
    return (
        len(
            panel.find_elements(
                By.CSS_SELECTOR,
                '[class*="events-tree-table"] [class*="arrow-down"]',
            )
        )
        != 0
    )


if __name__ == "__main__":
    print(
        get_html_from_page(
            category="E-sports +",
            sport="Counter-Strike: Global Offensive",
        )
    )
