import os.path
import time

import requests
import retry
from typing import Union, Literal

import tqdm
from selenium.webdriver import Chrome

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
# set driver to be headless
options = webdriver.ChromeOptions()
options.add_argument('headless')

# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.implicitly_wait(10)
# driver.get("https://www.ssa.gov/oact/babynames/")


@retry.retry(tries=5, backoff=1.5, max_delay=60)
def make_request(year: int, number_or_pct: str):
    """
    :param year: Year to get data for, min 1879
    :param number_or_pct: Either number of births (n) or percentage of births (p)
    """

    return requests.post(url="https://www.ssa.gov/cgi-bin/popularnames.cgi", data={
        "year": year,
        "top": 1000,
        "number": number_or_pct,
        "token":"Submit"
    })

def get_most_popular_names(years:list[int],number_or_pct:Literal['p','n'], outdir:str):
    with tqdm.tqdm(total=len(years)) as pbar:

        for year in years:
            filename = f'{outdir}/{year}_{number_or_pct}.html'
            if os.path.exists(filename):
                pbar.update()
                continue

            pbar.desc = f"Getting data for year {year} ({number_or_pct})"
            page = make_request(year, number_or_pct)
            if page.status_code != 200:
                print(f"Error getting data for year {year}")
            else:
                with open(f'{outdir}/{year}_{number_or_pct}.html','w') as f:
                    f.write(page.text)
            pbar.update()
            time.sleep(1)


if __name__ == '__main__':
    get_most_popular_names(list(range(1887,2024)),'n','data')
    get_most_popular_names(list(range(1887,2024)),'p','data')