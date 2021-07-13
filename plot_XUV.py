'''
Author       : caobin
Date         : 2021-07-13 10:08:30
LastEditors  : caobin
LastEditTime : 2021-07-13 15:04:09
FilePath     : \my-python-code\plot_XUV.py
'''

#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-
# this code plot the XUV data from mdsplus


import MDSplus as mds
import numpy as np
import matplotlib.pyplot as plt
from east_mds import get_data as get


shot = input("input shot: ")
shot = int(shot)
begin = input('input the begin time: ')
if begin == '':
    begin = 0
else:
    begin = float(begin)
end = input('input the end time: ')
if end == "":
    end = 0
else:
    end = float(end)


[t, x] = get.data('PXUV1', shot)
index = np.where((t>=begin)&(t<=end))
t = t[index]

for i in range(2, 65):
    singal_name = 'Pxuv'
    