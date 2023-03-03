from selenium import webdriver
from selenium_stealth import stealth
# import requests
from bs4 import BeautifulSoup
import json
import time
# from pprint import pprint
from selenium.webdriver.common.by import By

def create_chrome_driver():
  #====== CHROME CONFIG ======#
  options = webdriver.ChromeOptions()
  # options.add_argument("start-maximized")
  # options.add_argument("--headless")

  options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
  options.add_experimental_option('useAutomationExtension', False)
  driver = webdriver.Chrome(options=options)

  stealth(driver,
          languages=["fr-FR", "fr"],
          vendor="Google Inc.",
          platform="Win32",
          webgl_vendor="Intel Inc.",
          renderer="Intel Iris OpenGL Engine",
          fix_hairline=True,
          )
  
  return driver

def get_leboncoin_page():

  driver = create_chrome_driver()

  category = "9" # Immobilier
  type_of_announce = "appartements"
  page = 1
  city = "Colmar"
  zip_code = "68000"
  perimeter = "20000"

  URL = f"https://www.leboncoin.fr/recherche?category={category}&text={type_of_announce}&locations={city}_{zip_code}_{perimeter}&page={page}"

  # headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"}

  # response = requests.get(URL, headers=headers)
  # response.raise_for_status()
  driver.get(URL)
  time.sleep(5)
  # driver.implicitly_wait(10)
  if driver.find_element(By.ID,"didomi-notice-agree-button").is_displayed():
    driver.find_element(By.ID,"didomi-notice-agree-button").click()
  time.sleep(5)

  page_content = driver.page_source

  soup = BeautifulSoup(page_content, "html.parser")
  json_content = soup.find("script", {"type":"application/json"}).text
  datas = json.loads(json_content)
  announces = datas["props"]["pageProps"]["searchData"]["ads"]

  # Printing datas if VERBOSE
  for announce in announces:
      # pprint(announce)
      print("Title: ", announce["subject"])
      print("Type: ", announce["attributes"]["real_estate_type"]["value_label"])
      print("Rooms: ", announce["attributes"]["rooms"]["value"])
      print("Floor number: ", str(announce["attributes"]["floor_number"]["value"]))
      print("Age: ", announce["attributes"]["immo_sell_type"]["value_label"])
      print("Announce type: ", announce["attributes"]["lease_type"]["value_label"])
      print("Energy rate: ", announce["attributes"]["energy_rate"]["value_label"])
      print("GES (gas emission): ", announce["attributes"]["ges"]["value_label"])
      print("Price: ", str(announce["price_cents"] / 100) + " €")
      print("Surface: ", str(announce["attributes"]["square"]["value"]) + " m²")
      print("Price / m²: ", str((announce["price_cents"] / 100) / announce["attributes"]["square"]["value"]) + " €")
      print("Image 1: ", announce["images"]["urls"][0])
      print("Link: ", announce["url"])
      print("City: ", announce["location"]["city"])
      print("Zip code: ", announce["location"]["zipcode"])
      print("Region: ", announce["location"]["region_name"])
      print("Department: ", announce["location"]["department_name"])
      print("Lat: ", announce["location"]["lat"])
      print("Lng: ", announce["location"]["lng"])
      print("Index date: ", announce["index_date"])
      print("First publication date: ", announce["first_publication_date"])
      print("-" * 100)
  
  time.sleep(100)
  driver.quit()