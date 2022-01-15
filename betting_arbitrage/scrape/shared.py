from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from definitions import ROOT_DIR


def get_chrome():
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


CHROME_DRIVER_PATH = ROOT_DIR / "scrape" / "chromedriver.exe"