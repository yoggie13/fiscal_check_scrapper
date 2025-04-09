from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.by import By
import pprint


def scrape_web_page(link):
    load_dotenv()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-features=UseSkiaRenderer")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)

    driver.find_element(By.XPATH, "//a[@href='#collapse-specs']").click()

    try:
        WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "tbody[data-bind='foreach: Specifications'] tr"))
        )
    except:
        print("Timeout: No rows found in tbody")
        return False

    soup = BeautifulSoup(driver.page_source, "html.parser")

    pib = soup.find("span", {"id": "tinLabel"}).text
    shop = soup.find("span", {"id": "shopFullNameLabel"}).text
    shop = shop.split("-")
    shopID = shop[0]
    shopName = shop[1]
    checkID = soup.find("span", {"id": "invoiceNumberLabel"}).text
    total = soup.find("span", {"id": "totalAmountLabel"}).text
    date = soup.find("span", {"id": "sdcDateTimeLabel"}).text
    shop = soup.find("span", {"id": "shopFullNameLabel"}).text
    
    table = soup.find("table", {"class": "table invoice-table"})
    tbody = table.find("tbody", {"data-bind": "foreach: Specifications"})

    trs = tbody.find_all("tr")
    items = []

    for tr in trs:
        names = tr.find("strong", {"data-bind": "text: Name"}).text.strip().split(" ")
        name = " ".join([names[i] for i in range(1, len(names)-1)])
        item = (
            name,
            float(tr.find("td", {"data-bind": "decimalAsText: Quantity"}).text.strip().replace(".", "").replace(",",".")),
            float(tr.find("td", {"data-bind": "decimalAsText: UnitPrice"}).text.strip().replace(".", "").replace(",",".")),
            float(tr.find("td", {"data-bind": "decimalAsText: Total"}).text.strip().replace(".", "").replace(",","."))
        )

        items.append(item)
        
    div = soup.findAll("div", {"class": "col-lg-12 text-center centered"})[1]
    billWithQR = div.find("pre")

    bill = billWithQR.text
    QR = billWithQR.find("img")['src'][21:]


    return {
        "PIB": pib.strip(),
        "shopID": shopID.strip(),
        "shopName": shopName.strip(),
        "id": checkID.strip(),
        "total" : total.strip(),
        "bill" : bill,
        "date" : date.strip(),
        "shop" : shop.strip(),
        "items" : items,
        "QR":QR
    }