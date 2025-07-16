import time
import random
from selenium.webdriver.common.action_chains import ActionChains
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 사용자 계정 정보
INSTAGRAM_ID = ""
INSTAGRAM_PW = ""
HASHTAG = "맛"

# 브라우저 실행
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)
driver.get("https://www.instagram.com/")
time.sleep(5)

# 로그인
login_id = "//input[@name='username']"
login_pw = "//input[@name='password']"
login_btn = "//button[@type='submit']"
driver.find_element(By.XPATH, login_id).send_keys(INSTAGRAM_ID)
time.sleep(5)
driver.find_element(By.XPATH, login_pw).send_keys(INSTAGRAM_PW)
time.sleep(5)
driver.find_element(By.XPATH, login_btn).click()
print("로그인 완료")
time.sleep(10)

# 검색창
search_icon = "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div/div/div[2]/div[2]/span/div/a/div"
search_input = "/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[1]/div/div/input"
wait.until(EC.element_to_be_clickable((By.XPATH, search_icon))).click()
time.sleep(10)
search_box = wait.until(EC.presence_of_element_located((By.XPATH, search_input)))
search_box.send_keys(f"#{HASHTAG}")
time.sleep(10)
search_box.send_keys(Keys.ENTER)
time.sleep(10)
search_box.send_keys(Keys.ENTER)
print("해시태그 검색 완료")
search_result = '/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]/div/div/div[2]/div/a[1]/div[1]'
driver.find_element(By.XPATH, search_result).click()
time.sleep(10)

# 게시물 로드
post_links = wait.until(
    EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/p/")]'))
)

# 게시물 중 하나 선택 후 클릭
if post_links:
    random_post = random.choice(post_links)
    driver.execute_script("arguments[0].scrollIntoView(true);", random_post)
    ActionChains(driver).move_to_element(random_post).click().perform()
    print("게시물 클릭 완료!")

    # 좋아요(X)
    like_btn = "//*[@aria-label='좋아요' or @aria-label='좋아요 취소']/ancestor::button"
    try:
        like = wait.until(EC.element_to_be_clickable((By.XPATH, like_btn)))
        driver.execute_script("arguments[0].click();", like)
        print("좋아요 완료")
    except Exception as e:
        print(f"좋아요 실패: {e}")

    # 댓글 작성(X)
    comment_box_xpath = "//textarea[@aria-label='댓글 달기...']"
    comment_submit_btn = "//button[text()='게시']"
    try:
        comment_box = wait.until(EC.presence_of_element_located((By.XPATH, comment_box_xpath)))
        comment_box.click()
        comment_box.send_keys("안녕하세요")
        time.sleep(1)
        submit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, comment_submit_btn)))
        submit_btn.click()
        print("댓글 작성 완료")
    except Exception as e:
        print(f"댓글 작성 실패: {e}")

else:
    print("게시물이 없습니다.")

time.sleep(10)
driver.quit()