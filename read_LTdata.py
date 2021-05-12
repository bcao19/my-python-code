import  urllib.request
import re
import csv
import os, sys
import xlrd
import xlwt


path = r'D:/test.xls'
if os.path.exists(path):
    os.remove(path)


url = r'http://202.127.204.30/PF1iframe.php'
res = urllib.request.urlopen(url)
html = res.read().decode('utf-8')
temp = re.findall(".*#000000>(.*)</font>.*", html)

P_PFin = float(temp[1])
P_CSin = float(temp[4])
P_PFout = float(temp[5])
T_PFout = float(temp[6])


url = r'http://202.127.204.30/TFiframe.php'
res = urllib.request.urlopen(url)
html = res.read().decode('utf-8')
temp = re.findall(".*#000000>(.*)</font>.*", html)
T_TFout = float(temp[11])


url = r'http://202.127.204.30/TCiframe.php'
res = urllib.request.urlopen(url)
html = res.read().decode('utf-8')
temp = re.findall(".*#000000>(.*)</font>.*", html)
T_TFcaseout = float(temp[34])


url = r'http://202.127.204.30/LPiframe.php'
res = urllib.request.urlopen(url)
html = res.read().decode('utf-8')
temp = re.findall(".*#000000>(.*)</font>.*", html)
T_outcryo = float(temp[1])
P_incryo = float(temp[4])
T_incryo = float(temp[8])


#data = [{'T_incryo':T_incryo, 'P_incryo':P_incryo, 'T_outcryo':T_outcryo, 'T_TFout':T_TFout, 'T_PFout':T_PFout, 'P_PFin':P_PFin, 'P_CSin':P_CSin, 'P_PFout':P_PFout, 'T_TFcaseout':T_TFcaseout}]
data = [T_incryo, P_incryo, T_outcryo, T_TFout, T_PFout, P_PFin, P_CSin, P_PFout, T_TFcaseout]
#headers = ['T_incryo', 'P_incryo', 'T_outcryo', 'T_TFout', 'T_PFout', 'P_PFin', 'P_CSin', 'P_PFout', 'T_TFcaseout']

workbook = xlwt.Workbook()
sheet = workbook.add_sheet('sheet1')
for i in range(0, len(data)):
    sheet.write(0, i, data[i])
workbook.save(path)


