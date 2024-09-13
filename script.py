from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
import json

def load_config(file_path):
    """設定ファイルの読み込み"""
    with open(file_path, 'r') as file:
        config = json.load(file)
        config = {key: value for key, value in config.items() if not key.startswith('_')}
    
    return config

def login(driver, email, password, action, target_ranking_url):
    """ログイン処理"""
    driver.get('https://myfans.jp/sign_in')

    print('年齢確認開始', '\n')
    time.sleep(2)
    yes_button = driver.find_element(By.XPATH, "//button[text()='はい']")
    yes_button.click()
    time.sleep(3)

    print('ログイン開始', '\n')
    
    # name属性でテキストボックスを特定して入力
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "password").send_keys(password)
    
    # "ログイン"というテキストが含まれるボタンを特定してクリック
    login_button = driver.find_element(By.XPATH, "//button[text()='ログイン']")
    login_button.click()
    time.sleep(3)

    if action == '1':
        # ログイン成功後、女性ランキング画面にリダイレクト
        print('ランキング画面に遷移', '\n')
        driver.get(target_ranking_url) 
    else:
        # ログイン成功後、女性ランキング画面にリダイレクト
        print('フォロー一覧画面に遷移', '\n')
        driver.get("https://myfans.jp/mw6pgs/follow?t=following") 
    time.sleep(5)

def follow(driver, max_follow_limit):
    """フォロー"""

    print('対象ユーザ特定開始')
    # ランキング一覧からランダムでフォロワーを漁るユーザを決定する
    user_list_div = driver.find_element(By.XPATH, "//div[@class='px-4 py-2']")
    a_tags = user_list_div.find_elements(By.XPATH, ".//a")
    
    target_a_tag = random.choice(a_tags)
    target_username = target_a_tag.find_element(By.XPATH, ".//h3").text
    target_url = target_a_tag.get_attribute("href").split('?')[0]
    
    print("対象ユーザ：" + target_username + " (" + target_url + ")", '\n')
    
    # フォロワー一覧へ遷移
    driver.get(target_url + "/follow")
    time.sleep(5)
    
    print('フォロー開始')
    print('新たにフォローする数:', max_follow_limit, '\n')
    follower_container = driver.find_element(By.CLASS_NAME, "px-4")
    
    followed_count = 0
    while followed_count < max_follow_limit:
        buttons = follower_container.find_elements(By.XPATH, ".//button[contains(@class, 'MuiButton-outlinedPrimary')]")
        
        if not buttons:
            print("フォロー可能なボタンが見つかりません。スクロールします...")
            scroll_and_wait(driver)
            continue
        
        for button in buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
                
                followed_count += 1
                print(f"フォロー成功: 現在のフォロー数 {followed_count}")
                time.sleep(2)
            except Exception as e:
                print("クリック失敗:", e)
                followed_count = max_follow_limit
                break

            if followed_count == max_follow_limit:
                break
    time.sleep(3)

def remove(driver, remove_percentage):
    """リムーブ"""
    print('リムーブ開始')

    # follower_container = driver.find_element(By.CLASS_NAME, "px-4")
    current_follow_count = int(driver.find_element(By.XPATH, "//div[@class='pl-1 text-xs font-light']").get_attribute("textContent"))
    print("現在のフォロー数：", current_follow_count)
    print("リムーブ割合：", remove_percentage, "%")

    remove_follow_count = int(current_follow_count * (remove_percentage / 100))
    print("リムーブするフォロー数：", remove_follow_count)

    remaining_follow_count = current_follow_count - remove_follow_count
    print("リムーブ後のフォロー数：", remaining_follow_count, '\n')
    
    follower_container = driver.find_element(By.CLASS_NAME, "px-4")
    
    removed_count = 0
    while removed_count < remove_follow_count:
        buttons = follower_container.find_elements(By.XPATH, ".//button[contains(@class, 'MuiButton-containedGray ')]")
        
        if not buttons:
            print("フォロー解除可能なボタンが見つかりません。スクロールします...")
            scroll_and_wait(driver)
            continue
        
        for button in buttons:
            try:
                driver.execute_script("arguments[0].click();", button)
                
                removed_count += 1
                print(f"リムーブ成功: 現在の解除数 {removed_count}")
                time.sleep(2)
            except Exception as e:
                print("クリック失敗:", e)
                removed_count = remove_follow_count
                break
            
            if removed_count == remove_follow_count:
                break
    time.sleep(5)
def scroll_and_wait(driver):
    """スクロールしてデータロードを待つ"""
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

def main():
    # 外部ファイルからスクリプト実行に必要な情報を読み込む
    config = load_config('config.json')
    email = config['email']
    password = config['password']
    target_ranking_url = config['target_ranking_url']
    max_follow_limit = config['max_follow_limit']
    remove_percentage = config['remove_percentage']

    while True:
        action = input("フォローは 1、リムーブは 2 を入力してください: ")
        if action == "1" or action == "2":
            break
        else:
            print("無効な入力です。1 または 2 を入力してください。")

    try:
        print('')
        print("スクリプト開始", '\n')
        driver = webdriver.Chrome()
        login(driver, email, password, action, target_ranking_url)
        if action == '1':
            follow(driver, max_follow_limit)
        else:
            remove(driver, remove_percentage)
        print('')
        print('正常終了')
    except ValueError:
        print("無効な入力です。数値を入力してください。")
    except Exception as e:
        print('')
        print("予期せぬエラーが発生しました:", e)
        print('異常終了')
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

