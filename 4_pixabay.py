from selenium import webdriver
from urllib.request import Request, urlopen

driver = webdriver.Chrome()
url = 'https://pixabay.com/ko/images/search/강아지/'
driver.get(url)

image_xpath = '/html/body/div[1]/div[1]/div/div[2]/div[3]/div/div/div[1]/div[1]/div/a/img'
image_url = driver.find_element('xpath', image_xpath).get_attribute('src')
print('image_url: ', image_url)

image_byte = Request(image_url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

f = open('red_dot_dog.jpg', 'wb') # 바이너리 쓰기 모드로 파일 열기
f.write(urlopen(image_byte).read()) # 이미지 데이터 저장
f.close() # 파일 닫기