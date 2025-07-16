import time
import os
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
mongo_uri = os.getenv("MONGO_URI")

# MongoDB 연결 설정
client = MongoClient(mongo_uri)
db = client["pixabay_db"]
collection = db["images"]

# 검색어와 저장 폴더 이름
keyword = "경복궁"
save_dir = f"downloads/{keyword}"

# 저장 폴더 없으면 생성
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 크롬 드라이버 실행
driver = webdriver.Chrome()
driver.get("https://pixabay.com/")
time.sleep(2)

# 검색어 입력
search_box_xpath = '/html/body/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/form/div[1]/input'
search_box = driver.find_element('xpath', search_box_xpath)
search_box.send_keys(keyword)
time.sleep(1)
search_box.send_keys(Keys.RETURN)
time.sleep(3)

# 전체 이미지 URL 저장
all_image_urls = []

# 이미지 수집 함수
def collect_image_urls():
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1.5)

    image_area_xpath = '/html/body/div[1]/div[1]/div/div[2]/div[3]'
    image_area = driver.find_element('xpath', image_area_xpath)
    image_elements = image_area.find_elements('tag name', 'img')

    urls = []
    for img in image_elements:
        src = img.get_attribute('src')
        if src and src.startswith("https") and "blank.gif" not in src:
            urls.append(src)
    return urls

# 페이지 반복 수집
page_num = 1
while True:
    print(f"\n{page_num}페이지 이미지 수집 중")
    urls = collect_image_urls()
    all_image_urls.extend(urls)
    print(f"→ 현재까지 수집된 이미지 수: {len(all_image_urls)}")

    try:
        next_btn = driver.find_element('css selector', 'a[rel="next"]')
        driver.execute_script("arguments[0].click();", next_btn)
        time.sleep(3)
        page_num += 1
    except NoSuchElementException:
        print("\n마지막 페이지입니다.")
        break

driver.quit()

# 이미지 다운로드 함수 정의
def download_image(url, save_path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open(save_path, 'wb') as out_file:
            out_file.write(response.read())
        return True
    except Exception as e:
        print(f"{url} 저장 실패: {e}")
        return False

# 이미지 다운로드 및 MongoDB 저장
print("\n이미지 다운로드 및 MongoDB 저장 시작")
for idx, url in enumerate(all_image_urls, 1):
    ext = os.path.splitext(url)[1].split("?")[0] or ".jpg"
    filename = f"{keyword}_{idx}{ext}"
    local_path = os.path.join(save_dir, filename)

    if download_image(url, local_path):
        print(f"{filename} 저장 완료")

        # MongoDB에 저장
        doc = {
            "keyword": keyword,
            "index": idx,
            "image_url": url,
            "local_path": local_path.replace("\\", "/")
        }
        collection.insert_one(doc)

print("\n모든 이미지 다운로드 및 MongoDB 저장 완료!")