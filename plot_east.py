#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module plot the east data 
caobin@ipp.ac.cn 2020/1/2
add filter @ 20210512
test for github
"""



import tkinter as tk
import matplotlib.pyplot as plt
import numpy as np
from east_mds import get_data as get
from east_mds import  filter





window=tk.Tk() #创建Tk对象
window.title("plot shot signal") #设置窗口标题
window.geometry("275x300") #设置窗口尺寸
names = locals()
names['shot0'] = tk.Label(window,text="shot", height=1) #标签
names['shot0'].place(x=20, y=10) #指定包管理器放置组件

for i in range(1, 6):
    names['shot'+str(i)] = tk.Entry()
    names['shot'+str(i)].place(x=10, y=10+25*i, width=50)
    

names['signal0'] = tk.Label(window,text="signal", height=1) #标签
names['signal0'].place(x=100, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['signal'+str(i)] = tk.Entry()
    names['signal'+str(i)].place(x=80, y=10+25*i, width=80)



names['tree0'] = tk.Label(window,text="tree", height=1) #标签
names['tree0'].place(x=200, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['tree'+str(i)] = tk.Entry()
    names['tree'+str(i)].place(x=180, y=10+25*i, width=80)

tmp = tk.Label(window, text='begin')
tmp.place(x=10, y=230)
begin = tk.Entry()
begin.place(x=50, y=230, width=40)

tmp = tk.Label(window, text='end')
tmp.place(x=100, y=230)
end = tk.Entry()
end.place(x=130, y=230, width=40)

tmp = tk.Label(window, text='filter')
tmp.place(x=180, y=240)
low_filter = tk.Entry()
low_filter.place(x=210, y=230, width=40)
up_filter = tk.Entry()
up_filter.place(x=210, y=250, width=40)





def get_input():
    shots = []
    signals = []
    trees = []

    for i in range(1, 6):
        shot = names['shot'+str(i)].get()
        
        if len(shot)>0:
            shot = int(shot)
            shots.append(shot)
        else:
            from MDSplus import Connection as CN
            cn = CN('mds.ipp.ac.cn')
            shot = cn.get("current_shot('east')")
            shot = int(shot)
            shots.append(shot)
            break

    for i in range(1, 8):
        signal = names['signal'+str(i)].get()
        tree = names['tree'+str(i)].get()

        if len(signal)>0:
            signals.append(signal)
            if len(tree) == 0:
                trees.append('east_1')
            else:
                trees.append(tree)

    begin_time = begin.get()
    end_time = end.get()
    if len(begin_time)==0:
        begin_time = 0
    if len(end_time)==0:
        end_time = 10
    begin_time = float(begin_time)
    end_time = float(end_time)

    low_frequency= low_filter.get()
    if len(low_frequency)==0:
        low_frequency = 0
    low_frequency= int(low_frequency)

    up_frequency= up_filter.get()
    if len(up_frequency)==0:
        up_frequency = 0
    up_frequency= int(up_frequency)
    

    return shots, signals, trees, begin_time, end_time, low_frequency, up_frequency



def plot_data():

    plt.figure(figsize=(9, 12))

    [shots, signals, trees, begin, end, low_filter, up_filter] = get_input()

    i = 0
    colors = ['b', 'r', 'g', 'k', 'y']
    n = len(signals)
    for signal in signals:
        tree = trees[i]
        i = i+1
        j = 0
        for shot in shots:
            color = colors[j]
            j = j+1
            [t, y] = get.data(signal, shot, tree=tree)

            # if shot == 98346:
            #     temp = np.array(t)
            #     temp = temp-7
            #     t = temp

            # if shot == 98351:
            #     temp =np.array(t)
            #     temp = temp-5.5
            #     t = temp
            
            index = np.where((t>=begin)&(t<=end))            
            t = t[index]
            y = y[index]


            if up_filter != 0:
                fs = 100/(t[100]-t[0])
                fs = int(fs)
                if low_filter == 0:
                    y = filter.high_pass(y, up_filter, fs)
                elif up_filter >= 0.5*fs:
                    y = filter.low_pass(y, low_filter, fs)
                else:
                    y = filter.band_stop(y, low_filter, up_filter, fs)
            
            
            judge = signal[0:2]
            if judge == "G1":
                temp = np.array(y)
                temp = 10**(temp*1.667-9.333)
                y = list(temp)
            elif judge == "PA" or judge == "PJ":
                temp = np.array(y)
                temp = 2e3*temp
                y = list(temp)
            elif judge == "PP" or judge == "PD":
                temp = np.array(y)
                temp = 2e4*temp
                y = list(temp)
            
            
            
            plt.subplot(n, 1, i)
            if i==1:
                plt.plot(t, y, color=color, label=str(shot))
                plt.legend()
                plt.grid()
            else:
                plt.plot(t, y, color=color)
                plt.grid()
            if j==1:
                if i==n:
                    plt.xlabel('time (s)')
                plt.ylabel(signal)
            # if i==1:
            #     tmp = 1.1*np.max(y)
            #     locationY
            #     locationX = begin+(end-begin)/6*j
            #     plt.text(locationX, locationY, str(shot), color=color, fontsize=12)



    plt.show()










enter = tk.Button(window,text="Enter",command=plot_data)
enter.place(x=110, y=260)

window.mainloop() #进入主循环
