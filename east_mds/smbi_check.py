'''
Description: 
Author: caobin
Date: 2021-06-20 18:14:58
Github: https://github.com/bcao19
LastEditors  : caobin
LastEditTime : 2021-08-18 15:19:36
'''
#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module check the smbi injection
caobin@ipp.ac.cn 2020/1/2
"""



import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from east_mds import get_data as get
import MDSplus as mds
from scipy.signal import savgol_filter
from east_mds import filter




def check(shot, whichone, small=1):
    Pam2P = 4.82e20
    kp = 4e5
    if small < -1:
        V = 2.0431e-4+3.78e-3
        if whichone > 3:
            V = 4e-4+3e-3
    else:
        V = 2.0431e-4
        if whichone > 3:
            V = 4e-4
        
    small = abs(small)
    if whichone == 3:
        signal_name = 'smbi3'
        if small == 1:
            gauge_name = 'PAS105'
            kp = 2e3
        elif small == 3:
            gauge_name = 'PAS103'
        else:
            gauge_name = 'JHF1'
    elif whichone == 2:
        signal_name = 'smbi2'
        if small == 1:
            gauge_name = 'PJS205'
            kp = 2e3
        elif small == 3:
            gauge_name = 'PJS203'
        else:
            gauge_name = 'PJS204'
    elif whichone == 4:
        V = 4e-4
        signal_name = 'smbi4'
        if small == 1:
            gauge_name = 'PDS1_2'
            kp = 2e4
        else:
            gauge_name ='PDS1_3'
    elif whichone == 5:
        V = 4e-4
        signal_name = 'smbi5'
        if small == 1:
            gauge_name = 'PDS1_2'
            kp = 2e4
        else:
            gauge_name ='PDS1_3'
    elif whichone == 6:
        V = 4e-4
        signal_name = 'smbi6'
        if small == 1:
            gauge_name = 'PPS1_2'
            kp = 2e4
        else:
            gauge_name ='PPS1_3'
    elif whichone == 7:
        V = 4e-4
        signal_name = 'smbi7'
        if small == 1:
            gauge_name = 'PPS1_2'
            kp = 2e4
        else:
            gauge_name ='PPS1_3'
    else:
        import sys
        sys.exit('SMBI No. error')




    [t, smbi] = get.data(signal_name, shot, tree='EAST')
    pressure = get.data1(gauge_name, shot, tree='EAST_1')
    pressure = kp*pressure


    if len(smbi)<4.7e4:
        n=0
        l=0
        p=0

    else:

        index = np.where(smbi>3)
        l = len(index[0])*1e-4

        stop_smbi = max(index[0])
        print(stop_smbi)

        # temp = smbi[1 : ]-smbi[ : -1]
        # index = np.where(temp>3)
        # n = len(index[0])
        t = t[index]
        temp = t[1 : ]-t[ : -1]
        index = np.where(temp>7e-4)
        n = len(index[0])+1


        pressure = savgol_filter(pressure, 1001, 3)
        len_p = len(pressure)
        p = np.mean(pressure[100:1100])-np.mean(pressure[stop_smbi+100:stop_smbi+200])
        p = abs(p)
        if p<1e2:
            p = 0
        else:
            p = p*V*Pam2P

    print(n)
    print(l)
    print(p)

    return n, l, p








if __name__ == '__main__':

    shot = input("input shot: ")
    shot = int(shot)
    whichone = input("input which SMBI: ")
    if whichone == "":
        whichone=2
    else:
        whichone = int(whichone)
    small = input("input gauge: ")
    if small == "":
        small = 1
    else:
        small = int(small)

    [n, l, p] = check(shot, whichone, small)
