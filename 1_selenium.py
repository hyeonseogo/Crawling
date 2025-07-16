# 구글 검색
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get('https://www.google.com')
search = driver.find_element("name", "q")
search.send_keys("날씨")
time.sleep(1)
search.send_keys(Keys.RETURN) # 엔터 키 입력 (검색 실행)

time.sleep(5)
