'''
@Description: 
@Author: caobin
@Date: 2019-09-20 09:22:22
@Github: https://github.com/bcao19
@LastEditors: caobin
@LastEditTime: 2019-12-26 14:57:21
'''
#!/usr/local/bin/python3
import os
import time
from selenium import webdriver

URL = 'http://202.127.204.30/zonghenew.php'
PIC_PATH = 'E:/'
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
    browser = webdriver.PhantomJS()
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
        
if __name__ == '__main__':
    screenshot_web()