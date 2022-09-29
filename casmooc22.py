
from auto import auto
import time

auto.computer_web_open(r"https://www.casmooc.cn/#/course/index")
time.sleep(3)
auto.computer_prtsc('Screencap.png')
auto.computer_matchImg_up_down('Screencap.png', 'start.png', 148)
time.sleep(3)
auto.computer_prtsc('Screencap.png')
auto.computer_matchImg_up_down('Screencap.png', 'ksxx.png', 148)
time.sleep(10)
auto.computer_ctrl_w()
time.sleep(10)
auto.computer_ctrl_w()

auto.computer_page_down()
