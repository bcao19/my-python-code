import cv2
from aip import AipOcr

""" 你的 APPID AK SK  图2的内容"""
APP_ID = '16848192'
API_KEY = 'wyqzxRWLMw0isoGlMZsM7DSV'
SECRET_KEY = 'HTmPrS1zry62b0oen1wQzzYVIbtaflgC'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

fname = '/data/screenshot.png'

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

image = get_file_content(fname)

""" 调用通用文字识别, 图片参数为本地图片 """
results = client.general(image)["words_result"]  # 还可以使用身份证驾驶证模板，直接得到字典对应所需字段

img = cv2.imread(fname)
for result in results:
    text = result["words"]
    location = result["location"]

    print(text)
    # 画矩形框
    cv2.rectangle(img, (location["left"],location["top"]), (location["left"]+location["width"],location["top"]+location["height"]), (0,255,0), 2)

cv2.imwrite(fname[:-4]+"_result.jpg", img)
