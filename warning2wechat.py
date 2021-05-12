import urllib.request
import re
import os, sys
import datetime
from wxpy import *


flag = 0
# 获取当前时间
now = datetime.datetime.now()
# 启动时间
# 启动时间为当前时间加5秒

bot = Bot()
sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, 0, 0)
flag_time =  datetime.datetime.now()
name1 = '余耀伟'
name2 = '王俊儒'

while (True):

    now = datetime.datetime.now()

    if now > sched_timer:

        url = r'http://202.127.204.30/VACNEWiframe.php'
        res = urllib.request.urlopen(url)
        html = res.read().decode('utf-8')
        temp = re.findall(".*ffffff>(.*)</font>.*", html)
        date_time = re.findall(".*DATE TIME:(.*)</B>.*", html)

        if now > flag_time:
            friend = bot.friends().search(name1)[0]
            friend.send(date_time)
            friend.send(temp[16])
            friend.send(temp[12])
            friend = bot.friends().search(name2)[0]
            friend.send(date_time)
            friend.send(temp[16])
            friend.send(temp[12])
            flag_time = datetime.datetime.now()+datetime.timedelta(hours=1)

        tmp = ''.join(date_time)
        date_time = datetime.datetime.strptime(tmp, "%Y-%m-%d %H:%M:%S")
        low_time = datetime.datetime.now()+datetime.timedelta(minutes=-30)
        up_time = datetime.datetime.now()+datetime.timedelta(minutes=30)
        if date_time > up_time:
            friend = bot.friends().search(name1)[0]
            friend.send('Warning time not right')
            friend = bot.friends().search(name2)[0]
            friend.send('Warning time not right')
            sched_timer = datetime.datetime.now()+datetime.timedelta(minutes=5)

        if date_time < low_time:
            friend = bot.friends().search(name1)[0]
            friend.send('Warning time delay')
            friend = bot.friends().search(name2)[0]
            friend.send('Warning time delay')
            sched_timer = datetime.datetime.now()+datetime.timedelta(minutes=5)
        

        if temp[16] == "OFF":
            G203 = 1000.
        else:
            G203 = float(temp[16])

        if G203 > 100.:
            friend = bot.friends().search(name1)[0]
            friend.send('Warning G2.3')
            friend = bot.friends().search(name2)[0]
            friend.send('Warning G2.3')
            sched_timer = datetime.datetime.now()+datetime.timedelta(minutes=1)



        if temp[12] == "OFF":
            G505 = 1000.
        else:
            G505 = float(temp[12])

        if G505 > 100:
            friend = bot.friends().search(name1)[0]
            friend.send('Warning G5.5')
            friend = bot.friends().search(name2)[0]
            friend.send('Warning G5.5')
            sched_timer = datetime.datetime.now()+datetime.timedelta(minutes=1)

        

