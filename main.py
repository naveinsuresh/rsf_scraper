from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

import csv
from csv import writer

import time
from datetime import datetime

import pytz

import pandas as pd

from keep_alive import keep_alive

PATH = "C:\Program Files (x86)\chromedriver.exe"

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

DRIVER_PATH = "/opt/homebrew/bin/chromedriver"
ser = Service("chromedriver")

# url = "https://recsports.berkeley.edu/rsf-weight-room-crowd-meter/"
url = "https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"

# Note -- may want to make this headless
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.set_capability("pageLoadStrategy", "none")


def get_per():
    # driver = webdriver.Chrome(service=ser, desired_capabilities=capa)
    driver = webdriver.Chrome(options=chrome_options)

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
    td = datetime.fromtimestamp(ts).strftime("%A, %B %d, %Y %I:%M:%S")
    td2 = datetime.strptime(td, "%A, %B %d, %Y %I:%M:%S")
    list = [get_per(), ts, utc_to_local(td2)]
    with open(file, "a") as object:
        write_to = writer(object)
        write_to.writerow(list)
        object.close()


local_tz = pytz.timezone("America/Los_Angeles")


def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_dt


def get_last_date():
    with open("data.csv", "r") as file:
        reader = csv.reader(file)
        for row in reversed(list(reader)):
            # Return the second element of the last row
            element = row[1]
            break
    return float(element)


def is_rsf_open():
    # driver = webdriver.Chrome(service=ser, desired_capabilities=capa)
    driver = webdriver.Chrome(options=chrome_options)

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
        if (time.time() - last_date) // 60 > 1:
            store("data.csv")
    return


if __name__ == "__main__":
    while True:
        if is_rsf_open():
            results = pd.read_csv("data.csv")
            if len(results) + 1 == 1:
                store("data.csv")
            else:
                run()
