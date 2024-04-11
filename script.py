from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

# 前処理
target_follow_count_input = input("フォローするユーザ数を入力してください: ")
try:
  # 入力値を整数に変換
  target_follow_count = int(target_follow_count_input)
except ValueError:
  # 入力値が整数に変換できない場合のエラーハンドリング
  print("無効な入力です。数値を入力してください。")

# ウェブサイトを開く
driver = webdriver.Chrome()
driver.get('https://candfans.jp/auth/login')

# ログイン
print('start!!')

## user_id or email を入力
input_id = driver.find_element(By.CLASS_NAME, "id-input")
input_id.send_keys("[user_id or email]") # ここに user_id or email を入力する

## password を入力
input_password = driver.find_element(By.CLASS_NAME, "password-input")
input_password.send_keys("[password]") # ここに password を入力する

## ログインボタンをクリック 
button_login = driver.find_element(By.CLASS_NAME, "red-button")
button_login.click()


# ホーム画面

## データ取得を待つ
time.sleep(5)

## 人気クリエーター一覧を取得
targetUserLength = random.randrange(1, 21)
for _ in range(targetUserLength):
  driver.find_element(By.CLASS_NAME, "pseudo-swiper-button-next").click()
  time.sleep(1)

target_creator = driver.find_element(By.CLASS_NAME, "swiper-slide-active")

## クリエイター名称取得
print('対象クリエイター:' + target_creator.find_element(By.CLASS_NAME, "user-name").text)

## クリエイター詳細画面に遷移
target_creator.find_element(By.TAG_NAME, "a").click()


# クリエイター詳細画面

## データ取得を待つ
time.sleep(5)

## フォロワー一覧を開く
driver.find_elements(By.CSS_SELECTOR, ".user-scores .counter")[1].click()
time.sleep(3)

## フォローする
click_count = 0
while click_count < target_follow_count:
  buttons = driver.find_elements(By.CSS_SELECTOR, ".user .follow-button")

  for button in buttons:
    try:
      # フォローボタンが表示されているか確認し、クリック
      if button.is_displayed():
        button.click()
        click_count += 1
        time.sleep(1)

        if click_count == target_follow_count:
          break;
    except Exception as err:
        # クリックに失敗した時は握りつぶす
        pass

  if click_count != target_follow_count:
    follower_list = driver.find_element(By.CLASS_NAME, "users")
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', follower_list)
    time.sleep(2)

# ブラウザを閉じる
driver.quit()

print('end!!')
