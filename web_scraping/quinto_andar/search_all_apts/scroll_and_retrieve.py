import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

API_URL = "https://www.quintoandar.com.br/alugar/imovel/rio-de-janeiro-rj-brasil?survey=profiling_survey_rent_v2&survey_origin=home"
API_URL = (
    "https://www.quintoandar.com.br/alugar/imovel/botafogo-rio-de-janeiro-rj-brasil"
)

HOUSE_CARD_CONTAINER_DIV_CLASSES = ["sc-1j6got4-0", "knZWOQ"]
HOUSE_CARD_DIV_CLASSES = ["sc-7fnxs3-0", "IUFUB"]
HOUSE_CARD_A_CLASSES = ["sc-isijxy-0", "fdxHEM"]
FOOTER_DOG_IMAGE_CLASSES = ["sc-bczRLJ", "fYhQxB", "Cozy__SpotIllustration"]


def get_page_content(api_url, scroll_times):

    driver = webdriver.Chrome(
        "/home/sush/Downloads/Compressed/chromedriver_linux64/chromedriver"
    )
    driver.get(api_url)

    # Getting div that defines scroll area:
    element_scroll = driver.find_element(By.CLASS_NAME, "sc-18lu2ht-0")
    element_scroll.click()

    # Getting image that defines footer:
    element_footer = driver.find_element(By.CLASS_NAME, FOOTER_DOG_IMAGE_CLASSES[-1])

    contents = []
    all_urls = []
    for _ in range(scroll_times):
        driver.execute_script(
            "return arguments[0].scrollIntoView(true);", element_footer
        )
        time.sleep(5)
        contents.append(driver.page_source)
        urls = parse_html_data(driver.page_source)
        all_urls += urls

    all_urls = list(set(all_urls))
    print(len(all_urls))

    content = driver.page_source

    driver.close()

    return content


def parse_html_data(page_content):

    soup = BeautifulSoup(page_content, "html.parser")

    urls = []
    all_aptos = soup.findAll("a", {"class": ["sc-isijxy-0", "gjDuWo"]})
    for apto in all_aptos:
        href = apto.get("href")
        if href.startswith("/imovel"):
            urls.append(href)
    print(urls)
    print(len(urls))

    return urls


# for y in range(0, 1001, 250):
x = get_page_content(api_url=API_URL, scroll_times=5)
# parse_html_data(x)
