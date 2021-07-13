'''
Description: 
Author: caobin
Date: 2021-07-13 22:27:24
Github: https://github.com/bcao19
LastEditors: caobin
LastEditTime: 2021-07-13 23:22:35
'''

#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-
# this code for calculate the elm frequency

import numpy as np
import matplotlib.pyplot as plt
from east_mds import get_data as get


def find_peak(x, minx=0, maxx=0):
    if maxx == 0:
        maxx = max(x)
    divx1 = x[1 : -1]-x[ : -2]
    divx2 = x[1 : -1]-x[2 : ]
    n = len(divx1)
    judge = np.zeros(n+1)
    for i in range(n):
        if divx1[i]>0 and divx2[i]<0:
            if x[i+1]>minx and x[i+1]<=maxx:
                judge[i+1]=1
    
    index = np.where(judge == 1)

    return index


def cal_f(t):
    n = len(t)
    f = np.zeros(n+1)
    for i in range(n):
        f(i+1) = 1/(t[i+1]-t[i])
    f[0] = f[1]

    return f



