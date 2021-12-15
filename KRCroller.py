#from GrabzIt import GrabzItImageOptions
#from GrabzIt import GrabzItClient
from time import sleep
from selenium import webdriver
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
import glob
#grabzIt = GrabzItClient.GrabzItClient("MGVjZTRkY2E0ZGE1NGFhYjgxNjlhYzViYjE4YTljZTg=", "Pz8/IT8IP0w/ETICPwcMPyM/Pz8/dz9AUj8bTz9cUmk=")

# The 250 parameters indicates that image should be sized to 250 x 250 px
#options = GrabzItImageOptions.GrabzItImageOptions()
#options.width = 365.02
#options.height = 430
#options.format = "jpg"
#options.targetElement = "#weather"

#grabzIt.URLToImage("https://www.kma.go.kr/m/nation/forecast.jsp?ampm=1#none", options)
# Then call the Save or SaveTo method
###grabzIt.SaveTo("result.jpg")
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
    driver.get('https://www.kweather.co.kr/weather.html')
    driver.maximize_window()

    kweather_map = driver.find_element_by_class_name('kweather_map')

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
    photo = open("./kweather.png", 'rb')

except Exception as e:
    print(e)
    driver.quit()

finally:
    print("finally...")
    driver.quit()

img_array = []
for filename in glob.glob('kweather.png'):
    img = cv2.imread(filename)
    height, width, layers = img.shape
    size = (width,height)
    img_array.append(img)


out = cv2.VideoWriter('project.mp4',cv2.VideoWriter_fourcc(*'mp4v'), 15, size)

for i in range(len(img_array)):
    out.write(img_array[i])
out.release()



#####GC Push
from googleapiclient.http import MediaFileUpload
from Google import Create_Service

CLIENT_SECRET_FILE = 'client_secret.json'
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_SERVICE_NAME, API_VERSION, SCOPES)
file_id = '1w-7UVrM51OP0Imvrx-u0ffCiyq3UqfR7'

media_content = MediaFileUpload('project.mp4', mimetype='video/mp4')

service.files().update(
    fileId=file_id,
    media_body=media_content
).execute()
############################ OSError: [WinError 10048] 각 소켓 주소(프로토콜/네트워크 주소/포트)는 하나만 사용할 수 있습니다
###########데스크탑에(같은폴더)Google.py 놔두니 실행되버
