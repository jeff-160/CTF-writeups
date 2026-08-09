import os
import sys
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


timeout = int(os.environ["TIMEOUT"])
chromedriver = os.environ["DRIVER"]
chrome = os.environ["CHROME"]


def options():
    opts = Options()
    opts.binary_location = chrome

    for argument in (
        "--headless=new",
        "--disable-gpu",
        "--disable-popup-blocking",
        "--window-size=1920x1080",
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-background-networking",
    ):
        opts.add_argument(argument)

    return opts


def driver():
    service = Service(
        executable_path=chromedriver,
        port=0,
    )
    return webdriver.Chrome(service=service, options=options())


def visit(url):
    session = driver()

    try:
        session.get(url)
        time.sleep(timeout / 1000)
    finally:
        session.quit()


def main():
    if len(sys.argv) < 2:
        raise SystemExit("nope")

    visit(sys.argv[1])

if __name__ == "__main__":
    main()
