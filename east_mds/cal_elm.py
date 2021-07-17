'''
Description: 
Author: caobin
Date: 2021-07-13 22:27:24
Github: https://github.com/bcao19
LastEditors  : caobin
LastEditTime : 2021-07-17 14:29:16
'''

#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-
# this code for calculate the elm frequency

import numpy as np
import matplotlib.pyplot as plt
from east_mds import get_data as get


def find_peak(x, win=10, minx=0, maxx=0, percent=90):
    if maxx == 0:
        maxx = max(x)
    
    n = len(x)
    judge = np.zeros(n)
    for i in range(1, n-1):
        if x[i]-x[i-1]>0 and x[i]-x[i+1]>=0:
            if x[i]>minx and x[i]<=maxx:
                left = i-win
                if left<0:
                    left = 0
                left = int(left)
                left2 = i-100*win
                if left2<0:
                    left2 = 0
                left2 = int(left2)
                right = i+win
                if right>n+1:
                    right = n+1
                right = int(right)
                right2 = i+100*win
                if right2>n+1:
                    right2 = n+1
                right2 = int(right2)
                if x[i]>=max(x[left:right]) and x[i]>np.percentile(x[left2:right2], percent):
                    judge[i]=1
    
    index = np.where(judge == 1)

    return index


def cal_f(t):
    n = len(t)-1
    f = np.zeros(n+1)
    for i in range(n):
        f[i+1] = 1/(t[i+1]-t[i])
    f[0] = f[1]

    return f



def find_base(x, win, percent=90):
    xbase = np.zeros(len(x), dtype=float)
    for i in range(len(x)):
        left = i-win
        if left<0:
            left = 0
        left = int(left)
        right = i+win
        if right>len(x):
            right = len(x)
        right = int(right)
        xbase[i] = np.percentile(x[left:right], percent)

    return xbase





def cal_dw(t, x, threshold=1):
    dx1 = x[1 : -1]-x[: -2]
    dx2 = x[1 : -1]-x[2 :]
    index1 = np.where((dx1>=0) & (dx2>0))
    index1 = index1[0]+1
    index2 = np.where((dx1<=0) & (dx2<0))
    index2 = index2[0]+1
    dw = np.zeros(len(index1))
    for i in range(len(index1)):
        index = np.where(index2>index1[i])
        if len(index[0])>0:
            index = index[0][0]
            up_index = index1[i]
            low_index = index2[index]
            dw[i] = (x[up_index]-x[low_index])/1e3

    t = t[index1]
    index = np.where(dw>threshold)
    t = t[index]
    dw = dw[index]

    return t, dw






if __name__ == '__main__':

    signal = input('Input the signal: ')
    if signal == "":
        signal = 'dal1'
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
    else:
        threshold_list=threshold.split(",")
        threshold = [float(threshold_list[i]) for i in range(len(threshold_list))]
    win = input('Input the window for check in ms: ')
    if win=="":
        win = 1.0
    else:
        win = float(win)
    percent = input('Input the percent(0~100): ')
    if percent=="":
        percent = 90
    else:
        percent = float(percent)
    onlybase = input('Just plot base line(1 for ture, 0 for false): ')
    if onlybase=="":
        onlybase = -1
    else:
        onlybase = int(onlybase)
    dw_threshold = input('Input the dw_threshold: ')
    if dw_threshold == "":
        dw_threshold = 0
    else:
        dw_threshold = float(dw_threshold)


    

    if dw_threshold == 0:
        [t, x] = get.data(signal, shot, tree=tree, timerange=timerange)
        win = win//(t[1000]-t[0])

        if onlybase<=0:
            if onlybase == 0:
                xbase = find_base(x, 100*win, percent)

            n = len(threshold)-1
            if n==0:
                threshold.append(max(x))
                n = 1

            colors = ['r', 'g', 'c', 'm', 'y']
            plt.figure(figsize=(6, 7))
            plt.subplot(2, 1, 2)
            plt.plot(t, x)

            if onlybase == 0:
                plt.plot(t, xbase, color='b', linewidth=2)
            
            plt.xlabel('time (s)')
            plt.ylabel(signal)
            plt.xlim(begin_time, end_time)
            plt.subplot(2, 1, 1)
            plt.ylabel('ELM frequency (Hz)')
            plt.xlim(begin_time, end_time)

            for i in range(n):
                
                index = find_peak(x, win, threshold[i], threshold[i+1], percent)
                f_elm = cal_f(t[index])
                plt.subplot(2, 1, 2)
                plt.scatter(t[index], x[index], s=40, facecolors='none', edgecolors=colors[i])
                plt.subplot(2, 1, 1)
                plt.scatter(t[index], f_elm, s=40, facecolors='none', edgecolors=colors[i])


        else:
            xbase = find_base(x, 100*win, percent)
            plt.figure
            plt.plot(t, x)
            plt.xlabel('time (s)')
            plt.ylabel(signal)
            plt.xlim(begin_time, end_time)
            plt.plot(t, xbase, color='b', linewidth=2)


    else:
        [t, x] = get.data(signal, shot, tree=tree, timerange=timerange)
        win = win//(t[1000]-t[0])

        if onlybase<=0:
            if onlybase == 0:
                xbase = find_base(x, 100*win, percent)

            n = len(threshold)-1
            if n==0:
                threshold.append(max(x))
                n = 1

            colors = ['r', 'g', 'c', 'm', 'y']
            plt.figure(figsize=(6, 9))
            plt.subplot(3, 1, 3)
            plt.plot(t, x)

            if onlybase == 0:
                plt.plot(t, xbase, color='b', linewidth=2)
            
            plt.xlabel('time (s)')
            plt.ylabel(signal)
            plt.xlim(begin_time, end_time)
            plt.subplot(3, 1, 2)
            plt.ylabel('ELM frequency (Hz)')
            plt.xlim(begin_time, end_time)
            plt.subplot(3, 1, 1)
            plt.ylabel(r'ELM $\delta$w (kJ)')
            plt.xlim(begin_time, end_time)

            [td, dw] = cal_dw(t, x, dw_threshold)

            for i in range(n):
                
                index = find_peak(x, win, threshold[i], threshold[i+1], percent)
                f_elm = cal_f(t[index])
                dw_index = np.zeros(len(index[0]))
                for i in range(len(index[0])):
                    tmp = np.where(td>index[0][i])
                    if len(tmp[0])>0:
                        dw_index[i] = tmp[0][0]

                plt.subplot(3, 1, 3)
                plt.scatter(t[index], x[index], s=40, facecolors='none', edgecolors=colors[i])
                plt.subplot(3, 1, 2)
                plt.scatter(t[index], f_elm, s=40, facecolors='none', edgecolors=colors[i])
                plt.scatter(t[index], dw[dw_index], s=40, facecolors='none', edgecolors=colors[i])


        else:
            xbase = find_base(x, 100*win, percent)
            plt.figure
            plt.plot(t, x)
            plt.xlabel('time (s)')
            plt.ylabel(signal)
            plt.xlim(begin_time, end_time)
            plt.plot(t, xbase, color='b', linewidth=2)



    plt.show()
