from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from io import BytesIO
import requests
import json
import os

try:

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("lang=ko_KR")
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")

    # chrome driver
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(3)

    # 기상청 접속
    driver.get('https://m.kma.go.kr/m/nation/forecast.jsp?ampm=1')
    driver.maximize_window()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'nation_map posi2')))

    kweather_map = driver.find_element(By.CLASS_NAME,"nation_map posi2")

    location = kweather_map.location
    size = kweather_map.size

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    sleep(3)

    png = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(png))
    # 날씨 영역만 
    area = (left, top, right, bottom)
    kweather = img.crop(area)
    kweather.save('kweather.png')
    photo = open("./kweather.png", 'rb')


except Exception as e:
    print(e)    
    driver.quit()

finally:
    print("finally...")
    driver.quit()
    
