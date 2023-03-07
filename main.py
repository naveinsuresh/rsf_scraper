from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

from csv import writer

import time
from datetime import datetime

PATH = "C:\Program Files (x86)\chromedriver.exe"

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

DRIVER_PATH = "/opt/homebrew/bin/chromedriver"
ser = Service(DRIVER_PATH)

# url = "https://recsports.berkeley.edu/rsf-weight-room-crowd-meter/"
url = "https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"


def get_per():
    driver = webdriver.Chrome(service=ser, desired_capabilities=capa)

    driver.get(url)
    wait = WebDriverWait(driver, 20)

    # time.sleep(5)
    try:
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, ".styles_name__UKYcm"), text_="Weight Rooms"
            )
        )
    except TimeoutException:
        pass

    driver.execute_script("window.stop();")

    resp = driver.page_source

    soup = BeautifulSoup(resp, "html.parser")
    res = soup.find_all("span")

    for e in res:
        if "Full" in e.text:
            return int(e.text[: e.text.find("%")])
    return -1


def store(file):
    # take in a .csv file, file, append get_per() to the .csv file
    # store not only get_per but also the timestamp collected
    ts = time.time()
    list = [get_per(), ts]
    with open(file, "a") as object:
        write_to = writer(object)
        write_to.writerow(list)
        object.close()


def get_last_date():
    with open("data.csv", "r", encoding="utf-8", errors="ignore") as dime:
        final_line = dime.readlines()[-1]
    print(final_line)


def is_rsf_open():
    driver = webdriver.Chrome(service=ser, desired_capabilities=capa)

    driver.get("https://www.google.com/search?q=rsf+open+now")
    wait = WebDriverWait(driver, 20)

    # time.sleep(5)
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".wDYxhc")))
    except TimeoutException:
        pass

    driver.execute_script("window.stop();")

    resp = driver.page_source

    soup = BeautifulSoup(resp, "html.parser")
    # print(soup.find_all("div", {"class":"wDYxhc", "data-attrid": "kc:/location/location:hours"})[0])
    # print(soup.find_all("span", {"class":"JjSWRd"}))
    res = soup.find_all("span", {"class": "JjSWRd"})
    # print(res)

    for e in res:
        if "Closed" in e.text:
            # print(e.text)
            return False
    return True


def run():
    # check if it is currently open
    # check last data entry
    # if it's been more than a minite since last entry, call store
    if is_rsf_open():
        last_date = get_last_date()
        if time - last_date // 60 > 1:
            store("data.csv")
    return
