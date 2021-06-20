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
    else:
        V = 2.0431e-4
        
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
    else:
        signal_name = 'smbi2'
        if small == 1:
            gauge_name = 'PJS205'
            kp = 2e3
        elif small == 3:
            gauge_name = 'PJS203'
        else:
            gauge_name = 'PJS204'

    [ts, smbi] = get.data(signal_name, shot, 'EAST_1')
    [tp, pressure] = get.data(gauge_name, shot, 'EAST_1')
    pressure = kp*pressure


    if len(smbi)<4.7e3:
        n=0
        l=0
        p=0

    else:

        index = np.where(smbi>2)
        l = len(index[0])*1e-3
        temp = smbi[1 : ]-smbi[ : -1]
        index = np.where(temp>2)
        n = len(index[0])

        pressure = savgol_filter(pressure, 1001, 3)
        len_p = len(pressure)
        p = np.mean(pressure[100:1100])-min(pressure[int(len_p-1e4-100):int(len_p-1e4)])
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
    whichone = int(whichone)
    small = input("input gauge: ")
    small = int(small)
    [n, l, p] = check(shot, whichone, small)
