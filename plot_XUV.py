'''
Author       : caobin
Date         : 2021-07-13 10:08:30
LastEditors: caobin
LastEditTime: 2021-07-13 20:31:19
FilePath     : \my-python-code\plot_XUV.py
'''

#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-
# this code plot the XUV data from mdsplus


from scipy import signal
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


[t, x] = get.data('Pxuv1', shot, tree='EAST_1')
index = np.where((t>=begin)&(t<=end))
tP = t[index]

Pxuv = np.zeros([64, len(tP)], dtype=float)
Pxuv[0, :] = x[index]

for i in range(1, 64):
    signal_name = 'Pxuv'
    signal_name = signal_name+str(i+1)
    x = get.data1(signal_name, shot, 'EAST_1' )
    Pxuv[i, :] = x[index]



[t, x] = get.data('Cxuv1V', shot, tree='EAST_1')
index = np.where((t>=begin)&(t<=end))
tC = t[index]

Cxuv = np.zeros([40, len(tC)], dtype=float)
Cxuv[0, :] = x[index]

for i in range(1, 40):
    signal_name = 'Cxuv'
    signal_name = signal_name+str(i+1)+'V'
    x = get.data1(signal_name, shot, 'EAST_1')
    Cxuv[i, :] = x[index]



vmax = np.percentile(Pxuv, 90)
plt.figure()
plt.pcolormesh(tP, list(range(1, 65)), Pxuv, vmax=vmax, cmap='jet')
plt.title('Pxuv')
plt.ylabel('Channel')
plt.xlabel('Time [sec]')
plt.colorbar()



vmax = np.percentile(Cxuv, 90)
plt.figure()
plt.pcolormesh(tC, list(range(1, 41)), Cxuv, vmax=vmax, cmap='jet')
plt.title('Cxuv')
plt.ylabel('Channel')
plt.xlabel('Time [sec]')
plt.colorbar()


plt.show()