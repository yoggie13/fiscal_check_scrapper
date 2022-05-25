from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os


def scrape_web_page(link):
    load_dotenv()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    div = soup.find("div", {"class": "col-lg-12 text-center centered"})
    bill = div.find("pre")

    print(bill.text)


scrape_web_page("https://suf.purs.gov.rs/v/?vl=A1BQRjNXSlBGUFBGM1dKUEYkBgAAEAYAAICxTwEAAAAAAAABgPazDQkAAAA%2B59pYYr0w1EhwZHmYmvJ%2BByEb6q%2BcJaUG7k%2BaZioUb1v2xxGBujVbHmNcJ45fuZTydRC1OERWglbuvZxcPRvQZibHEYrgYyqgOlCuKqrZUP%2FdM5RmtAlNJMx73i1tqgsh0EkaLN38jlEPK74AJZ3Bib300NPTroD0wEwVTM1mc4HwZ4Y0VozJsayn3P%2F3DBGIBpxbIOaq16QjOloZzI5GXVDciR%2FWGKSngkXYufaAHJuoFMZZz32nhAmVO5HmdyLBjds5UiIl8t4Ch5jHISjnOuyh7SaFx%2Fiktzc%2BoqDO5P%2B0nktDipq%2BAHhGmlrje8Wp%2FBu%2B2hn%2BsYNviXrFbQ2LSRYsDOGCd2k5aj6EVS2ec0O2IHlL%2BNxgkwnk8Nv6elUt9Nul3fgrXcU%2FhsOZH9UtuOArpIz70Ai6ZLYzLNhJGVOw0SLfAl9yROOWvJ0sD8NS51RHVCyxn2a1DbcR2cNiZN3rNvGxiPLSRJLbhEkebdHQay2jgUOgzYiCivY6z54RB2CRkwKoAgs%2F%2FggOUy6nM%2F6lPytwJXgQkVAdqrRXxBk7ygxOl%2F%2F889GeV94kUhVY05yk5WjKvPNwreVuIkjKdAfWcrt76yF9b49%2BdYbRLHEv9snXbwi8F8pg8oucgWvlCcedV3rLiRiy6EDaQd20DVzQqFFtx2DPidNl1ZYzsm1ByUf6TyIQxsio9Y79FAw%3D")
