from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def scrape_web_page(link):
    load_dotenv()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(executable_path="C:\\chromeData\\chromedriver.exe", options=chrome_options)
    driver.get(link)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    div = soup.findAll("div", {"class": "col-lg-12 text-center centered"})[1]
    bill = div.find("pre")

    print(bill.text)
