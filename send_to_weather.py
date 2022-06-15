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
import glob
import cv2

try:

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("lang=ko_KR")
    options.add_argument('headless')
    options.add_argument('window-size=410x700')
    options.add_argument("disable-gpu")
    options.add_argument("--no-sandbox")

    # chrome driver
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.implicitly_wait(3)

    # 기상청 접속
    #driver.get('https://m.kma.go.kr/m/nation/forecast.jsp?ampm=1')
    driver.get('https://www.weather.go.kr/w/index.do')
    driver.maximize_window()
    
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'weather')))

    kweather_map = driver.find_element(By.ID,"content_weather")

    location = kweather_map.location
    size = kweather_map.size

    left = location['x']
    top = location['y']
    right = location['x'] + size['width']
    bottom = location['y'] + size['height']
    sleep(3)
    
 #   path = './update'
 #   os.mkdir(path)
    
    png = driver.get_screenshot_as_png()
    img = Image.open(BytesIO(png))
    # 날씨 영역만 
    area = (left, top, right, bottom)
    kweather = img.crop(area)
    kweather.save('./kweather.png')
    photo = open("./kweather.png", 'rb')
    
    #mp4 convert
    img_array = []
    for filename in glob.glob('./kweather.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
        
    out =  cv2.VideoWriter('./kweather.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 60, size)
    
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    
    
    
except Exception as e:
    print(e)    
    driver.quit()

finally:
    print("finally...")
    driver.quit()
    
