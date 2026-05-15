from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from dotenv import load_dotenv
import os
from pathlib import Path

# =========================
# 설정
# =========================
env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(dotenv_path=env_path)
email = os.getenv("ID")
PASSWORD = os.getenv("PASSWORD")
MATTERMOST_URL = os.getenv("MATTERMOST_URL")

EMOJI_NAME = "pepe"
IMAGE_PATH = r"C:\emoji\pepe.png"

# =========================
# 드라이버 실행
# =========================

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install())
)

wait = WebDriverWait(driver, 15)

# =========================
# 로그인 페이지 이동
# =========================

driver.get(f"{MATTERMOST_URL}login")
## 한번 더 누르기
time.sleep(2.5)
wait.until(
    EC.presence_of_element_located(
    (By.CSS_SELECTOR,
    f'a[href="{MATTERMOST_URL}login"]'))
).click()


# =========================
# 로그인
# =========================

login_input = wait.until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[id="input_loginId"], input[class="form-control"]'))
)
login_input.send_keys(email)

password_input = driver.find_element(By.CSS_SELECTOR, 'input[id="input_password-input"]')
password_input.send_keys(PASSWORD)

submit_btn = driver.find_element(By.CSS_SELECTOR, "#saveSetting")
submit_btn.click()

# =========================
# 로그인 완료 대기
# =========================


# =========================
# 커스텀 이모지 페이지 이동
# =========================

wait.until(
    EC.element_to_be_clickable(
        (By.ID, "emojiPickerButton")
    )
).click()
# =========================
# "Add Custom Emoji" 버튼 클릭
# =========================

wait.until(
    EC.element_to_be_clickable(
        (By.XPATH, "//span[text()='Custom Emoji']")
    )
).click()





time.sleep(1.5)
#################
## 이미지 연속 업로드 시작
##########
## 이름 적기
IMAGE_FOLDER = "output"

files = os.listdir(IMAGE_FOLDER)

for file in files:

    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//span[text()='이모티콘 추가']")
        )
    ).click()


    if not file.endswith((".png", ".jpg", ".jpeg", ".gif")):
        continue

    emoji_name = os.path.splitext(file)[0]

    image_path = os.path.abspath(
        os.path.join(IMAGE_FOLDER, file)
    )

    name_input = wait.until(
        EC.presence_of_element_located((By.ID, 'name'))
    )
    name_input.send_keys(emoji_name)

    file_input = wait.until(
        EC.presence_of_element_located(
            (By.ID, 'select-emoji')
        )
    )
    file_input.send_keys(image_path)
    driver.find_element(
        By.XPATH,
        "//span[text()='저장']"
    ).click()


