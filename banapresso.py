import time
import os
import requests
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as BS
from dotenv import load_dotenv

def get_coords_google(address, api_key):
    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        lat = location["lat"]
        lon = location["lng"]
        return lat, lon
    else:
        print(f"주소를 찾을 수 없습니다: {address}")
        print(f"상태 코드: {data['status']}")
        return None, None

def crawling_banapresso_stores(url, google_api_key):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    driver.maximize_window()

    prev_store_count = 0

    while True:
        scroll_area = driver.find_element(By.XPATH, '//*[@id="contents"]/article/div/div[1]/div[2]')
        for _ in range(10):
            scroll_area.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.05)

        soup = BS(driver.page_source, 'html.parser')
        time.sleep(1)
        stores = soup.find_all('li', class_='storeSidebarItem__SidebarItem-sc-10wrqox-0 jsFpcE')

        if len(stores) == prev_store_count:
            break
        prev_store_count = len(stores)

    store_html = soup.find_all('span', class_='store_name_map')
    parsed = BS(str(store_html), 'html.parser')

    store_data = []
    for name, addr in zip(parsed.select('span > i'), parsed.select('span > span')):
        store_name = name.get_text(strip=True)
        address = addr.get_text(strip=True)

        lat, lon = get_coords_google(address, google_api_key)

        store_data.append({
            'store_name': store_name,
            'address': address,
            'latitude': lat,
            'longitude': lon
        })

        print(f"{store_name} | {address} | 위도: {lat}, 경도: {lon}")

    driver.quit()
    return store_data

url = "https://www.banapresso.com/store"
load_dotenv()
google_api_key = os.getenv("Google_API_KEY")
store_list = crawling_banapresso_stores(url, google_api_key)

df = pd.DataFrame(store_list)
df.to_csv("banapresso_store_with_coords.csv", index=False, encoding="utf-8-sig")
print("데이터가 banapresso_store_with_coords.csv 파일로 저장되었습니다.")
