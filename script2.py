from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

def login(driver, user_id, password):
    """ログイン処理"""
    driver.get('https://candfans.jp/auth/login')
    print('start!!')
    driver.find_element(By.CLASS_NAME, "id-input").send_keys(user_id)
    driver.find_element(By.CLASS_NAME, "password-input").send_keys(password)
    driver.find_element(By.CLASS_NAME, "red-button").click()

def follow_random_creators(driver, target_follow_count):
    """ランダムにクリエーターをフォローする"""
    time.sleep(5)  # ログイン後の読み込み待ち

    targetUserLength = random.randrange(1, 21)
    for _ in range(targetUserLength):
        driver.find_element(By.CLASS_NAME, "pseudo-swiper-button-next").click()
        time.sleep(1)

    target_creator = driver.find_element(By.CLASS_NAME, "swiper-slide-active")
    print('対象クリエイター:' + target_creator.find_element(By.CLASS_NAME, "user-name").text)
    target_creator.find_element(By.TAG_NAME, "a").click()

    time.sleep(5)  # クリエイター詳細画面の読み込み待ち
    driver.find_elements(By.CSS_SELECTOR, ".user-scores .counter")[1].click()
    time.sleep(3)  # フォロワー一覧モーダルの読み込み待ち

    click_count = 0
    while click_count < target_follow_count:
        buttons = driver.find_elements(By.CSS_SELECTOR, ".user .follow-button")
        for button in buttons:
            if button.is_displayed():
                try:
                    button.click()
                    click_count += 1
                    time.sleep(1)
                except Exception as e:
                    print("クリック失敗:", e)
                if click_count == target_follow_count:
                    break
        if click_count != target_follow_count:
            scroll_and_wait(driver)

def scroll_and_wait(driver):
    """スクロールしてデータロードを待つ"""
    follower_list = driver.find_element(By.CLASS_NAME, "users")
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', follower_list)
    time.sleep(2)

def main():
    user_id = input("User ID or Email: ")
    password = input("Password: ")
    target_follow_count_input = input("フォローするユーザ数を入力してください: ")
    try:
        target_follow_count = int(target_follow_count_input)
        driver = webdriver.Chrome()
        login(driver, user_id, password)
        follow_random_creators(driver, target_follow_count)
    except ValueError:
        print("無効な入力です。数値を入力してください。")
    except Exception as e:
        print("予期せぬエラーが発生しました:", e)
    finally:
        driver.quit()
        print('end!!')

if __name__ == "__main__":
    main()

