from time import sleep
from selenium import webdriver
from PIL import Image
from io import BytesIO
import requests
import json

try:

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("lang=ko_KR")
    options.add_argument('headless')
    options.add_argument('window-size=1920x1080')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")

    # chrome driver
    driver = webdriver.Chrome('chromedriver', chrome_options=options)
    driver.implicitly_wait(3)

    # 케이웨더 접속
    driver.get('https://m.kma.go.kr/m/nation/forecast.jsp?ampm=1')
    driver.maximize_window()

    kweather_map = driver.find_element_by_class_name('nation_map posi2')

    location = kweather_map.location
    size = kweather_map.size

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    sleep(3)

    png = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(png))
    # 오늘의 날씨 영역만 잘라냅니다.
    area = (left, top, right, bottom)
    kweather = img.crop(area)
    kweather.save('kweather.png')



except Exception as e:
    print(e)    
    driver.quit()

finally:
    print("finally...")
    driver.quit()
    
