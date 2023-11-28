import time

import requests
import retry
from typing import Union

from selenium.webdriver import Chrome

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(10)
driver.get("https://www.ssa.gov/oact/babynames/")



@retry.retry(tries=5, backoff=1.5, max_delay=60)
def make_request(year: int, number: str):
    return requests.post(url="https://www.ssa.gov/cgi-bin/popularnames.cgi", data={
        "year": year,
        "top": 1000,
        "number": number
    })
