#!/usr/local/bin/python3
import time
from selenium import webdriver
from wxpy import *
import urllib.request
import os, sys
import datetime
from PIL import Image


URL = 'http://202.127.204.30/Vacuumnew.php'
PIC_PATH = os.path.join(os.path.expanduser('~'), 'Pictures/python/screenshot') 
PIC_NAME = 'screenshot.png'


def screenshot_web(url=URL, path=PIC_PATH, name=PIC_NAME):
    '''capture the whole web page
    :param url: the website url
    :type url: str
    :param path: the path for saving picture
    :type str
    :param name: the name of picture
    :type name: str
    '''
    if not os.path.exists(path):
        os.makedirs(path)

    browser = webdriver.Chrome('E:/chromedriver.exe')
    browser.set_window_size(1200, 800)
    browser.get(url)
    time.sleep(3)
    pic_path = os.path.join(os.path.join(path, name))
    print(pic_path)
    if browser.save_screenshot(pic_path):
        print('Done!')
    else:
        print('Failed!')
    browser.close()
        

bot = Bot()

flag = 0
# 获取当前时间
now = datetime.datetime.now()
# 启动时间
# 启动时间为当前时间加1小时
sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, 0, 0) 




while (True):
    
    now = datetime.datetime.now()
    # print(type(now))
    # 本想用当前时间 == 启动时间作为判断标准，但是测试的时候 毫秒级的时间相等成功率很低 而且存在启动时间秒级与当前时间毫秒级比较的问题
    # 后来换成了以下方式，允许10分之差
    
    if (sched_timer < now < sched_timer + datetime.timedelta(minutes=50)) & (flag==0):

        screenshot_web()
        pic_path = os.path.join(os.path.join(PIC_PATH, PIC_NAME))
        wxpy_groups = bot.groups().search('真空组工作群')
        group = wxpy_groups[0]
        group.send_image(pic_path)
        screenshot_web('http://202.127.204.30/zonghenew.php')
        img = Image.open(pic_path)
        cropped = img.crop((600, 421, 1100, 660))
        cropped.save(pic_path)
        group.send_image(pic_path)

        



        


        flag = 1



    else:
        
        
        if flag==1:
            # 修改定时任务时间 时间间隔为3小时
            sched_timer = sched_timer + datetime.timedelta(hours=3)
            flag = 0
