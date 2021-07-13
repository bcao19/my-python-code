'''
Description: 
Author: caobin
Date: 2021-07-13 22:27:24
Github: https://github.com/bcao19
LastEditors: caobin
LastEditTime: 2021-07-14 01:11:00
'''

#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-
# this code for calculate the elm frequency

import numpy as np
import matplotlib.pyplot as plt
from east_mds import get_data as get


def find_peak(x, win=10, minx=0, maxx=0):
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
    n = len(t)-1
    f = np.zeros(n+1)
    for i in range(n):
        f[i+1] = 1/(t[i+1]-t[i])
    f[0] = f[1]

    return f



if __name__ == '__main__':

    signal = input('Input the signal: ')
    if signal == "":
        signal = 'dau2'
    tree = input('Input the tree: ')
    if tree == "":
        tree = 'east'
    shot = input('Input the shot: ')
    shot = int(shot)
    begin_time = input('Input the begin_time: ')
    begin_time = float(begin_time)
    end_time = input('Input the end_time: ')
    end_time = float(end_time)
    timerange = [begin_time, end_time]
    threshold = input('Please input the threshold value: ')
    if threshold == "":
        threshold = [0]
    threshold_list=threshold.split(",")
    threshold = [float(threshold_list[i]) for i in range(len(threshold_list))]
    threshold = np.array(threshold)

    [t, x] = get.data(signal, shot, tree=tree, timerange=timerange)

    n = len(threshold)-1
    if n==0:
        threshold = [threshold, max(x)]
        n = 1

    colors = ['b', 'r', 'g', 'k', 'y']
    plt.figure(figsize=(9, 12))
    plt.subplot(2, 1, 2)
    plt.plot(t, x)

    for i in range(n):
        index = find_peak(x, threshold[i], threshold[i+1])
        f_elm = cal_f(t[index])
        plt.subplot(2, 1, 2)
        plt.scatter(t[index], x[index], s=80, facecolors='none', edgecolors=colors[i])
        plt.subplot(2, 1, 1)
        plt.scatter(t[index], f_elm, s=80, facecolors='none', edgecolors=colors[i])

    plt.show()
