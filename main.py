from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service

import time

PATH = 'C:\Program Files (x86)\chromedriver.exe'

capa = DesiredCapabilities.CHROME
capa["pageLoadStrategy"] = "none"

DRIVER_PATH = "/opt/homebrew/bin/chromedriver"
ser = Service(DRIVER_PATH)

#url = "https://recsports.berkeley.edu/rsf-weight-room-crowd-meter/"
url = "https://safe.density.io/#/displays/dsp_956223069054042646?token=shr_o69HxjQ0BYrY2FPD9HxdirhJYcFDCeRolEd744Uj88e"

def get_per():
    driver=webdriver.Chrome(service=ser, desired_capabilities=capa)

    driver.get(url)
    wait = WebDriverWait(driver, 20)

    #time.sleep(5)
    try:
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '.styles_name__UKYcm'), text_='Weight Rooms'))
    except TimeoutException:
        pass

    driver.execute_script("window.stop();")

    resp = driver.page_source

    soup = BeautifulSoup(resp, "html.parser")
    res = soup.find_all("span")

    for e in res:
        if "Full" in e.text:
            return int(e.text[:e.text.find("%")])
    return -1

def store(file):
    # take in a .csv file, file, append get_per() to the .csv file
    # store not only get_per but also the timestamp collected


def run():
    # check if it is currently open
    # check last data entry
    # if it's been more than a minite since last entry, call store




