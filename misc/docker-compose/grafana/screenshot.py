
# 日本語フォントインストール
#!apt-get -y install fonts-ipafont-gothic
#!apt-get -y install fonts-ipafont-mincho

# seleniumインストール
#!apt-get update
#!apt install chromium-chromedriver
#!cp /usr/lib/chromium-browser/chromedriver /usr/bin
#!pip install selenium

# ライブラリインポート
import time
import datetime
import shutil
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chromeヘッドレスモード起動
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('chromedriver',options=options)
driver.implicitly_wait(10)

# 対象URL
urls = [
        'http://localhost:3000/d/A7xFebgVz/dosue-y?orgId=1&refresh=10s&from=now-5m&to=now',
        'http://localhost:3000/d/A7xFebgVz/dosue-y?orgId=1&refresh=10s&from=now-30m&to=now',
        'http://localhost:3000/d/A7xFebgVz/dosue-y?orgId=1&refresh=10s&from=now-1h&to=now',
        'http://localhost:3000/d/A7xFebgVz/dosue-y?orgId=1&refresh=10s&from=now-3h&to=now',
        'http://localhost:3000/d/A7xFebgVz/dosue-y?orgId=1&from=1663746180000&to=now',
        'http://localhost:3000/d/3w7HW4h4z/tandem?orgId=1&from=now-3h&to=now',
        'http://localhost:3000/d/fXdQAzp4z/dosue-pi?orgId=1&from=now-3h&to=now',
        ]

# ファイル名接頭辞
fileNamePrefix = "screenshot"

# ウインドウ幅指定
# 初期値: False, スマホ: 375
# windowSizeWidth = False
windowSizeWidth = 1600

# ウインドウ高さ指定
# 初期値: False
#windowSizeHeight = False
windowSizeHeight = 1200

# 連番初期値
shotNum = 0

# ダウンロードフォルダ作成
folderCheck = os.path.exists('output')
if not folderCheck:
  os.mkdir('output')
  pass


try:

  # 繰り返し処理
  for i, url in enumerate(urls):
    # パス指定
    folderPath = 'output/' + fileNamePrefix + '-'   

    # サイトURL取得
    driver.get(url)
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
    
    # ウインドウ幅・高さ指定
    windowWidth = driver.execute_script('return document.body.scrollWidth;')
    if windowSizeWidth and (windowWidth<windowSizeWidth):
        windowWidth = windowSizeWidth
        pass
    windowHeight = driver.execute_script('return document.body.scrollHeight;')
    if windowSizeHeight and (windowHeight < windowSizeHeight):
        windowHeight = windowSizeHeight
        pass
    driver.set_window_size(windowWidth, windowHeight)
   
    # スクロール処理
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
   
    # 処理後一時待機
    time.sleep(2)
   
    # スクリーンショット格納
    filename = f'{folderPath}{i:02d}.png'
    print(f'{datetime.datetime.now()} create a screenshot: {filename}')
    print(f'    from {url}')
    driver.save_screenshot(filename)
   
    # サーバー負荷軽減処理
    time.sleep(1)

    pass # End of loop
   
  # ブラウザ稼働終了
  driver.quit()

except Exception as e:
  print(f'Error in getting screenshot for {url}')
  print(f'Error: {e}')
  driver.quit()
