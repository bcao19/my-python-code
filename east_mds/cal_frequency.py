'''
Description: 
Author: caobin
Date: 2021-06-16 09:01:57
Github: https://github.com/bcao19
LastEditors: caobin
LastEditTime: 2021-07-10 15:21:41
'''
#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module will calculate the frequency
caobin@ipp.ac.cn 2019/12/30
"""

from scipy import signal
from east_mds import get_data as get
import numpy as np
import matplotlib.pyplot as plt

def spec_stft(t, x, nfft=1024, vmax=0.002):


    dt = (t[22]-t[2])/20
    ts=dt*1000
    fs=1/ts
    from scipy import signal
    f, tf, Zxx = signal.stft(x, fs, nperseg=nfft, noverlap=nfft//2, detrend='constant')
    tf = tf/1000+t[0]
    Zxx = np.abs(Zxx)
    Zxx[0:1,:]=0
    vmin =0
    if vmax == -1:
        Zxx = np.log10(Zxx)-np.log10(np.max(Zxx))
        vmax = np.max(Zxx)
        vmin = np.min(Zxx)


    return tf, f, Zxx, vmin, vmax



if __name__ == '__main__':

    signal = input('Input the signal: ')
    if signal == "":
        signal = 'kmp14t'
    shot = input('Input the shot: ')
    shot = int(shot)
    tree = input('Input the tree: ')
    if tree == "":
        tree = 'east'
    begin_time = input('Input the begin_time: ')
    begin_time = float(begin_time)
    end_time = input('Input the end_time: ')
    end_time = float(end_time)
    method = input('Input the method: ')
    if method == "":
        method = 'stft'
    nfft = input('Input the number for fft: ')
    if nfft == "":
        nfft = 1024
    else:
        nfft = int(nfft)
    fcut = input("Input the cut off high frequency: ")
    if fcut == "":
        fcut = 0
    else:
        fcut = float(fcut)
    vmin = input('Input the vmin: ')
    if vmin == "":
        vmin = 0
    else:
        vmin = float(vmin)
    vmax = input('Input the vmax: ')
    if vmax == "":
        vmax = 0
    else:
        vmax = float(vmax)


    [t, x] = get.data(signal, shot, tree)
    index = np.where((t>=begin_time)&(t<=end_time))
    t = t[index]
    x = x[index]

    if method == 'stft':
        [tf, f, Zxx, vmin, vmax] = spec_stft(t, x, nfft, vmax)
    if vmax == 0:
        vmax = np.percentile(Zxx, 90)
        print(vmax)


    plt.figure()
    plt.pcolormesh(tf, f, Zxx, vmin=vmin, vmax=vmax, cmap='jet')
    plt.title(signal)
    plt.ylabel('Frequency [kHz]')
    plt.xlabel('Time [sec]')
    plt.colorbar()
    if fcut != 0:
        plt.ylim([0, fcut])

    plt.show()