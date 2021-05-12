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

def spec_stft(signal, shot, tree, timerange, vmax=0.002, fcut=0):
    [t, x] = get.data(signal, shot, tree)
    index = np.where((t>timerange[0])&(t<timerange[1]))
    t = t[index]
    x = x[index]
    nfft = 1024

    dt = (t[22]-t[2])//20
    ts=dt*1000
    fs=1/ts
    f, tf, Zxx = signal.stft(x, fs, nperseg=nfft, noverlap =nfft//2, detrend='constant')
    tf = tf+timerange[0]
    Zxx = np.abs(Zxx)
    Zxx[0:1,:]=0
    vmin =0
    if vmax == -1:
        Zxx = np.log10(Zxx)-np.log10(np.max(Zxx))
        vmax = max(Zxx)
        vmin = min(Zxx)

    plt.figure()
    plt.pcolormesh(tf, f, Zxx, vmin=vmin, vmax=vmax, cmap='jet')
    plt.title('STFT Magnitude')
    plt.ylabel('Frequency [Hz]')
    lt.xlabel('Time [sec]')
    plt.colorbar()
    if fcut != 0:
        pllt.ylim([0, fcut])

    plt.show

    return tf, f, Zxx



if __name__ == '__main__':
	
	signal = input('Input the signal: ')
    shot = input('Input the shot: ')
    shot = int(shot)
    tree = input('Input the tree: ')
    method = input('Input the method: ')

    if methon == 'stft':
        