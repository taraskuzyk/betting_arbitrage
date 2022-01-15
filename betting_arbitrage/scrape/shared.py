import datetime
from dataclasses import dataclass

import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from database.orm.sport import Sport
from database.orm.website import Website
from definitions import ROOT_DIR


def get_chrome():
    return undetected_chromedriver.Chrome()
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument(f"--window-size={dimensions.width}x{dimensions.height}")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/96.0.4664.110 Safari/537.36"
    )
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    return webdriver.Chrome(
        chrome_options=chrome_options, executable_path=str(CHROME_DRIVER_PATH)
    )


@dataclass
class Bet:
    team_1_name: str
    team_2_name: str
    team_1_odds: float
    team_2_odds: float
    sport: Sport
    website: Website
    match_datetime: datetime.datetime = None
    tournament_name: str = None


CHROME_DRIVER_PATH = ROOT_DIR / "scrape" / "chromedriver.exe"
