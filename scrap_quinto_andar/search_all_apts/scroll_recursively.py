import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

API_URL = "https://www.quintoandar.com.br/alugar/imovel/rio-de-janeiro-rj-brasil?survey=profiling_survey_rent_v2&survey_origin=home"

HOUSE_CARD_DIV_CLASSES = ["sc-7fnxs3-0", "IUFUB"]
HOUSE_CARD_A_CLASSES = ["sc-isijxy-0", "fdxHEM"]


def get_page_content(api_url):

    driver = webdriver.Chrome(
        "/home/sush/Downloads/Compressed/chromedriver_linux64/chromedriver"
    )
    driver.get(api_url)

    SCROLL_PAUSE_TIME = 2

    # Getting div (scroll area) and footer elements (to be used for scrolling):
    element_scroll = driver.find_element(By.CLASS_NAME, "sc-18lu2ht-0")
    element_footer = driver.find_element(By.CLASS_NAME, "sc-bczRLJ")

    # Get scroll height:
    # last_height = driver.execute_script("return document.body.scrollHeight")
    last_height = element_scroll.get_attribute("scrollHeight")
    print("last_height", last_height)

    while True:
        # Scroll down to bottom
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script(
            "return arguments[0].scrollIntoView(true);", element_footer
        )

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        # new_height = driver.execute_script("return document.body.scrollHeight")
        new_height = element_scroll.get_attribute("scrollHeight")
        print("new_height", new_height)
        if new_height == last_height:
            break
        last_height = new_height

    content = driver.page_source

    driver.close()

    return content


def parse_html_data(page_content):

    soup = BeautifulSoup(page_content, "html.parser")
    # print(soup)

    # all_aptos = soup.findAll("div", {"class": "sc-7fnxs3-0"})
    # print(all_aptos[1])

    urls = []
    all_aptos = soup.findAll("a", {"class": ["sc-isijxy-0", "gjDuWo"]})
    for apto in all_aptos:
        href = apto.get("href")
        if "imovel" in href:
            print(apto, "\n")
            urls.append(href)
    """
    for apto in all_aptos:
        link = apto.findAll("a", {"class": "sc-isijxy-0"})
        if link:
            urls.append(apto.a.get("href"))
    """
    # print(urls)
    print(len(urls))

    return


x = get_page_content(API_URL)
y = parse_html_data(x)

import pickle

with open("html_content.pickle", "wb") as f:
    pickle.dump(x, f)

with open("html_content.txt", "w", encoding="utf-8") as f:
    f.write(str(x))
