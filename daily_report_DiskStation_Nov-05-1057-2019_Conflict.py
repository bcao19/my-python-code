####从网页读取真空数据，每小时存一次


import urllib.request
import re
import csv
import os, sys
import xlrd
import xlwt
from xlutils.copy import copy
import datetime
import psutil

judge = 0
pids = psutil.pids()
for pid in pids:
    p = psutil.Process(pid)
    if p.name() == 'daily_report.exe':
        judge = judge+1

if judge>2:
    os._exit()




path = os.getcwd()
path = path+'\\daily_report.xls'


flag = 0
# 获取当前时间
now = datetime.datetime.now()
# 启动时间
# 启动时间为当前时间加5秒
sched_timer = datetime.datetime(now.year, now.month, now.day, now.hour, 1, 0) 


while (True):

    now = datetime.datetime.now()
    # print(type(now))
    # 本想用当前时间 == 启动时间作为判断标准，但是测试的时候 毫秒级的时间相等成功率很低 而且存在启动时间秒级与当前时间毫秒级比较的问题
    # 后来换成了以下方式，允许1秒之差
    
    if (sched_timer < now < sched_timer + datetime.timedelta(minutes=59)) & (flag==0):
        

        url = r'http://202.127.204.30/VACNEWiframe.php'
        res = urllib.request.urlopen(url)
        html = res.read().decode('utf-8')
        temp = re.findall(".*ffffff>(.*)</font>.*", html)
        date_time = re.findall(".*DATE TIME:(.*)</B>.*", html)


        if temp[0] == "OFF":
            G503 = 0.
        else:
            G503 = float(temp[0])

        if temp[1] == "OFF":
            G501 = 0.
        else:
            G501 = float(temp[1])

        if temp[2] == "OFF":
            G507 = 0.
        else:
            G507 = float(temp[2])

        if temp[4] == "OFF":
            G204 = 0.
        else:
            G204 = float(temp[4])

        if temp[7] == "OFF":
            G107 = 0.
        else:
            G107 = float(temp[7])

        if temp[9] == "OFF":
            G101 = 0.
        else:
            G101 = float(temp[9])

        if temp[10] == "OFF":
            G506 = 0.
        else:
            G506 = float(temp[10])

        if temp[11] == "OFF":
            G502 = 0.
        else:
            G502 = float(temp[11])

        if temp[12] == "OFF":
            G505 = 0.
        else:
            G505 = float(temp[12])

        if temp[15] == "OFF":
            G508 = 0.
        else:
            G508 = float(temp[15])

        if temp[16] == "OFF":
            G203 = 0.
        else:
            G203 = float(temp[16])

        if temp[18] == "OFF":
            G504 = 0.
        else:
            G504 = float(temp[18])


        vacuum = [date_time, G101, G107, G203, G204, G501, G504, G507, G503, G508, G505, G502, G506]



        url = r'http://202.127.204.30/VACNEW2iframe.php'
        res = urllib.request.urlopen(url)
        html = res.read().decode('utf-8')
        temp = re.findall(".*> (.*)</div>.*", html)
        date_time = re.findall(".*DATE TIME:(.*)</B>.*", html)

        TVVM = float(temp[3])
        TVVG = float(temp[10])
        THFJ = float(temp[11])
        TVVI = float(temp[13])
        TPG2 = float(temp[18])
        TPG1 = float(temp[19])
        TPG20 = float(temp[21])
        TPG18 = float(temp[22])
        TVHF = float(temp[37])


        url = r'http://202.127.204.30/VACTiframe.php'
        res = urllib.request.urlopen(url)
        html = res.read().decode('utf-8')
        temp = re.findall(".*000000>(.*)</font>.*", html)

        TVUP = 0
        TVLP = float(temp[14])

        temperature = [date_time, TVVG, TVVI, TVVM, THFJ, TPG1, TPG2, TPG18, TPG20, TVUP, TVHF, TVLP]



        if os.path.isfile(path):

            workbook = xlrd.open_workbook(path)  # 打开工作簿
            sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
            worksheet = workbook.sheet_by_name(sheets[0])  # 获取工作簿中所有表格中的的第一个表格
            rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
            new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象

            new_worksheet = new_workbook.get_sheet(0)  # 获取转化后工作簿中的第一个表格
            for i in range(0, len(vacuum)):
                new_worksheet.write(rows_old, i, vacuum[i])



            new_worksheet = new_workbook.get_sheet(1)  # 获取转化后工作簿中的第二个表格
            for i in range(0, len(temperature)):
                new_worksheet.write(rows_old, i, temperature[i])

            new_workbook.save(path)

        else:
            workbook = xlwt.Workbook()
            sheet = workbook.add_sheet('sheet1')
            for i in range(0, len(vacuum)):
                sheet.write(0, i, vacuum[i])
            sheet = workbook.add_sheet('sheet2')
            for i in range(0, len(temperature)):
                sheet.write(0, i, temperature[i])
            workbook.save(path)


        flag = 1


    else:
        
        
        if flag==1:
            # 修改定时任务时间 时间间隔为1小时
            sched_timer = sched_timer + datetime.timedelta(hours=1)
            flag = 0
            
