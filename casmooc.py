'''
Author       : caobin
Date         : 2021-12-02 15:20:08
LastEditors  : caobin
LastEditTime : 2021-12-02 16:00:15
FilePath     : \undefinedd:\bcao19\my-python-code\casmooc.py
'''

# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 13:03:32 2021

@author: caobin
"""


from auto import auto
import time
x_location = [450, 700, 950, 1200, 1450]
y_location = [260, 560, 850]
y1_location = [480, 760]
auto.computer_web_open('http://www.casmooc.cn//onlineStudy.do?method=intoFrame')


for y in y1_location:
    for x in x_location:
        time.sleep(3)
        auto.computer_click(x, y)
        time.sleep(3)
        auto.computer_prtsc('Screencap.png')
        if auto.computer_if_matchImg('Screencap.png', 'start.png'):
            auto.computer_matchImgClick('Screencap.png', 'start.png')
            time.sleep(3)
            auto.computer_prtsc('Screencap.png')
            if auto.computer_if_matchImg('Screencap.png', 'ksxx.png'):
                auto.computer_matchImgClick('Screencap.png', 'ksxx.png')
            time.sleep(600)
            auto.computer_ctrl_w()
            time.sleep(3)
            auto.computer_ctrl_w()
            
        else:
            time.sleep(3)
            auto.computer_ctrl_w()
            
            
    
time.sleep(3)
auto.computer_page_down()

for y in y_location:
    for x in x_location:
        time.sleep(3)
        auto.computer_click(x, y)
        auto.computer_prtsc('Screencap.png')
        if auto.computer_if_matchImg('Screencap.png', 'start.png'):
            auto.computer_matchImgClick('Screencap.png', 'start.png')
            time.sleep(3)
            auto.computer_prtsc('Screencap.png')
            if auto.computer_if_matchImg('Screencap.png', 'ksxx.png'):
                auto.computer_matchImgClick('Screencap.png', 'ksxx.png')
            time.sleep(600)
            auto.computer_ctrl_w()
            time.sleep(3)
            auto.computer_ctrl_w()
            time.sleep(3)
            
            
time.sleep(3)
auto.computer_page_down()

for y in y_location:
    for x in x_location:
        time.sleep(3)
        auto.computer_click(x, y)
        auto.computer_prtsc('Screencap.png')
        if auto.computer_if_matchImg('Screencap.png', 'start.png'):
            auto.computer_matchImgClick('Screencap.png', 'start.png')
            time.sleep(3)
            auto.computer_prtsc('Screencap.png')
            if auto.computer_if_matchImg('Screencap.png', 'ksxx.png'):
                auto.computer_matchImgClick('Screencap.png', 'ksxx.png')
            time.sleep(600)
            auto.computer_ctrl_w()
            time.sleep(3)
            auto.computer_ctrl_w()
            time.sleep(3)


for i in range(0, 10):
    time.sleep(3)
    auto.computer_prtsc('Screencap.png')
    auto.computer_matchImgClick('Screencap.png', 'xyy.png')

    for y in y1_location:
    for x in x_location:
        time.sleep(3)
        auto.computer_click(x, y)
        time.sleep(3)
        auto.computer_prtsc('Screencap.png')
        if auto.computer_if_matchImg('Screencap.png', 'start.png'):
            auto.computer_matchImgClick('Screencap.png', 'start.png')
            time.sleep(3)
            auto.computer_prtsc('Screencap.png')
            if auto.computer_if_matchImg('Screencap.png', 'ksxx.png'):
                auto.computer_matchImgClick('Screencap.png', 'ksxx.png')
            time.sleep(600)
            auto.computer_ctrl_w()
            time.sleep(3)
            auto.computer_ctrl_w()
            
        else:
            time.sleep(3)
            auto.computer_ctrl_w()
            
            
    
    time.sleep(3)
    auto.computer_page_down()

    for y in y_location:
        for x in x_location:
            time.sleep(3)
            auto.computer_click(x, y)
            auto.computer_prtsc('Screencap.png')
            if auto.computer_if_matchImg('Screencap.png', 'start.png'):
                auto.computer_matchImgClick('Screencap.png', 'start.png')
                time.sleep(3)
                auto.computer_prtsc('Screencap.png')
                if auto.computer_if_matchImg('Screencap.png', 'ksxx.png'):
                    auto.computer_matchImgClick('Screencap.png', 'ksxx.png')
                time.sleep(600)
                auto.computer_ctrl_w()
                time.sleep(3)
                auto.computer_ctrl_w()
                time.sleep(3)
                
                
    time.sleep(3)
    auto.computer_page_down()

    for y in y_location:
        for x in x_location:
            time.sleep(3)
            auto.computer_click(x, y)
            auto.computer_prtsc('Screencap.png')
            if auto.computer_if_matchImg('Screencap.png', 'start.png'):
                auto.computer_matchImgClick('Screencap.png', 'start.png')
                time.sleep(3)
                auto.computer_prtsc('Screencap.png')
                if auto.computer_if_matchImg('Screencap.png', 'ksxx.png'):
                    auto.computer_matchImgClick('Screencap.png', 'ksxx.png')
                time.sleep(600)
                auto.computer_ctrl_w()
                time.sleep(3)
                auto.computer_ctrl_w()
                time.sleep(3)