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

def get_meilleuragents_page():
  driver = create_chrome_driver()

  city = "colmar"
  zip_code = "68000"

  URL = f"https://www.meilleursagents.com/prix-immobilier/{city}-{zip_code}/"
  driver.get(URL)
  time.sleep(5)
  try:
    accept_cookie = driver.find_element(By.ID,"didomi-notice-agree-button")
    accept_cookie.click()
  except:
    pass
  time.sleep(5)

  page_content = driver.page_source
  # Extract real estate prices estimations
  soup = BeautifulSoup(page_content, "html.parser")
  prices_div = soup.find_all("ul", {"class": "prices-summary__price-range"})
  appartment_prices_mean = int(str(prices_div[0].find_all("li")[1].text).strip().replace("\n", "").replace("\u202f", "").replace("\xa0", "").replace(" ", "").replace("€", ""))
  appartment_prices_interval = str(prices_div[0].find_all("li")[2].text).strip().replace("\n", "").replace("\u202f", "").replace("\xa0", "").replace(" ", "").replace("de", "").replace("€", "").split("à")
  if len(appartment_prices_interval) == 1:
    for i in range(len(appartment_prices_interval)):
        appartment_prices_interval[i] = int(appartment_prices_interval[i])
    appartment_confidence_index = len(prices_div[0].find_all("li", {"class": "green"}))
    print("appartment_prices_mean: ", appartment_prices_mean)
    print("appartment_prices_min: ", appartment_prices_interval[0])
    print("appartment_prices_max: ", appartment_prices_interval[1])
    print("appartment_confidence_index: ", appartment_confidence_index)
  if len(prices_div) > 1:
    house_prices_mean = int(str(prices_div[1].find_all("li")[1].text).strip().replace("\n", "").replace("\u202f", "").replace("\xa0", "").replace(" ", "").replace("€", ""))
    house_prices_interval = str(prices_div[1].find_all("li")[2].text).strip().replace("\n", "").replace("\u202f", "").replace("\xa0", "").replace(" ", "").replace("de", "").replace("€", "").split("à")
    for i in range(len(house_prices_interval)):
      house_prices_interval[i] = int(house_prices_interval[i])
    house_confidence_index = len(prices_div[1].find_all("li", {"class": "green"}))
    print("house_prices_mean: ", house_prices_mean)
    print("house_prices_min: ", house_prices_interval[0])
    print("house_prices_max: ", house_prices_interval[1])
    print("house_confidence_index: ", house_confidence_index)

  # Type exact address and launch search
  driver.find_element(By.XPATH, "//input[@name='q'][@type='text']").send_keys("avenue montaigne, 75008 Paris")
  time.sleep(2)
  driver.find_element(By.XPATH, "//div[@class='tt-dataset-0']").click()
  time.sleep(5)

  driver.quit()

def get_leboncoin_page():

  driver = create_chrome_driver()

  category = "9" # Immobilier
  type_of_announce = "appartements"
  page = 1
  city = "Paris"
  zip_code = "75000"
  perimeter = "20000"

  URL = f"https://www.leboncoin.fr/recherche?category={category}&text={type_of_announce}&locations={city}_{zip_code}_{perimeter}&page={page}"

  # headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:86.0) Gecko/20100101 Firefox/86.0"}

  # response = requests.get(URL, headers=headers)
  # response.raise_for_status()
  driver.get(URL)
  time.sleep(5)
  # driver.implicitly_wait(10)
  try:
    accept_cookie = driver.find_element(By.ID,"didomi-notice-agree-button")
    accept_cookie.click()
  except:
    pass
  time.sleep(10)

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