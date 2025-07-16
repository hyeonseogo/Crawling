import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import quote
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get('https://www.instagram.com/')
soup = BeautifulSoup(driver.page_source, "html.parser")
time.sleep(5)

username_input = driver.find_element(By.NAME, "username")
password_input = driver.find_element(By.NAME, "password")

username_input.send_keys("crawling153")
time.sleep(2)
password_input.send_keys("000153153")
time.sleep(2)

login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
login_button.click()

time.sleep(15)

hashtag = "맛집탐방"
encoded_hashtag = quote(f"#{hashtag}")
url = f"https://www.instagram.com/explore/search/keyword/?q={encoded_hashtag}"

driver.get(url)

wait = WebDriverWait(driver, 15)

# 게시물만 로드될 때까지 기다림
post_links = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/p/")]'))
)

print(f"게시물 수: {len(post_links)}")

# 게시물 중 하나 무작위 선택 후 클릭
if post_links:
    random_post = random.choice(post_links)
    driver.execute_script("arguments[0].scrollIntoView(true);", random_post)
    ActionChains(driver).move_to_element(random_post).click().perform()
    print("무작위 게시물 클릭 완료!")
else:
    print("게시물이 없습니다.")

time.sleep(10)
# wait = WebDriverWait(driver, 10)

def open_post_in_new_tab_and_comment(driver, comment_text="좋아요!", wait_time=10):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    import time

    wait = WebDriverWait(driver, wait_time)

    try:
        # 게시물 링크 수집
        post_links = driver.find_elements(By.XPATH, '//a[contains(@href, "/p/")]')
        print(f"📌 게시물 개수: {len(post_links)}")

        if not post_links:
            print("❌ 게시물이 없습니다.")
            return

        post_url = post_links[0].get_attribute("href")
        print("➡️ 게시물 URL:", post_url)

        # 새 탭에서 열기
        driver.execute_script("window.open(arguments[0]);", post_url)
        driver.switch_to.window(driver.window_handles[-1])  # 새 탭으로 전환
        time.sleep(5)

        # 댓글 입력창이 나타날 때까지 기다림
        wait.until(EC.presence_of_element_located((By.XPATH, '//textarea[@aria-label="댓글 달기..."]')))
        comment_area = driver.find_element(By.XPATH, '//textarea[@aria-label="댓글 달기..."]')
        driver.execute_script("arguments[0].scrollIntoView(true);", comment_area)
        comment_area.click()
        time.sleep(1)
        comment_area.send_keys(comment_text)
        time.sleep(1)

        # 게시 버튼 클릭
        post_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="게시"]')))
        post_button.click()
        print("✅ 댓글 작성 완료!")

    except Exception as e:
        print(f"❌ 댓글 작성 실패: {e}")

open_post_in_new_tab_and_comment(driver, "정말 맛있어 보여요 😋")

# def click_like_button_safely(driver, wait_time=10):
#     try:
#         wait = WebDriverWait(driver, wait_time)

#         # 좋아요 아이콘이 포함된 svg의 부모 div(role=button) 탐색
#         like_button = wait.until(EC.element_to_be_clickable((
#             By.XPATH, '//section//svg[@aria-label="좋아요"]/ancestor::div[@role="button"]'
#         )))

#         # 스크롤 + JS 강제 클릭
#         driver.execute_script("arguments[0].scrollIntoView(true);", like_button)
#         driver.execute_script("arguments[0].click();", like_button)
#         print("✅ 좋아요 클릭 성공 (버튼 기준)")

#     except Exception as e:
#         print(f"❌ 좋아요 클릭 실패: {e}")

# click_like_button_safely(driver)

time.sleep(10)
