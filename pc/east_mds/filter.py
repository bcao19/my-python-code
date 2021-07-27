#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module will get the data from MDSplus and tranlate to array
caobin@ipp.ac.cn 2021/5/10
"""

__author__ = 'caobin'

from scipy import signal
import numpy as np


def band_stop(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], 'bandstop')  # 配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, data)  # data为要过滤的信号

    return filtedData


def band_pass(data, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = signal.butter(order, [low, high], 'bandpass')  # 配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, data)  # data为要过滤的信号

    return filtedData


def low_pass(data,  highcut, fs, order=5):
    nyq = 0.5 * fs
    
    high = highcut / nyq
    b, a = signal.butter(order, high, 'lowpass')  # 配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, data)  # data为要过滤的信号

    return filtedData


def high_pass(data,  lowcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    
    
    b, a = signal.butter(order, low, 'highpass')  # 配置滤波器 8 表示滤波器的阶数
    filtedData = signal.filtfilt(b, a, data)  # data为要过滤的信号

    return filtedData


def smooth(y, box_pts):        #smooth
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')

    return y_smooth