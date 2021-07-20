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
window.geometry("575x300") #设置窗口尺寸
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



names['label0'] = tk.Label(window,text="label", height=1) #标签
names['label0'].place(x=300, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['label'+str(i)] = tk.Entry()
    names['label'+str(i)].place(x=280, y=10+25*i, width=80)


names['process0'] = tk.Label(window,text="process", height=1) #标签
names['process0'].place(x=400, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['process'+str(i)] = tk.Entry()
    names['process'+str(i)].place(x=380, y=10+25*i, width=80)


names['parameter0'] = tk.Label(window,text="parameter", height=1) #标签
names['parameter0'].place(x=495, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['parameter'+str(i)] = tk.Entry()
    names['parameter'+str(i)].place(x=480, y=10+25*i, width=80)



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
    labels = []
    processes = []
    parameters = []

    for i in range(1, 6):
        shot = names['shot'+str(i)].get()
        
        if len(shot)>0:
            shot = int(shot)
            shots.append(shot)
        else:
            if i == 1:
                from MDSplus import Connection as CN
                cn = CN('mds.ipp.ac.cn')
                shot = cn.get("current_shot('east')")
                shot = int(shot)
                shots.append(shot)

    for i in range(1, 8):
        signal = names['signal'+str(i)].get()
        tree = names['tree'+str(i)].get()
        label = names['label'+str(i)].get()
        process = names['process'+str(i)].get()
        parameter = names['parameter'+str(i)].get()

        if len(signal)>0:
            signals.append(signal)
            if len(tree) == 0:
                trees.append('east_1')
            else:
                trees.append(tree)

            if len(label) == 0:
                labels.append(signal)
            else:
                labels.append(label)

            if len(process) == 0:
                processes.append('None')
                parameters.append('None')
            else:
                processes.append(process)
                if len(parameter) == 0:
                    parameters.append('None')
                else:
                    parameter_list=parameter.split(",")
                    parameter = [float(parameter_list[i]) for i in range(len(parameter_list))]
                    parameters.append(parameter)



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
    

    return shots, signals, trees, begin_time, end_time, low_frequency, up_frequency, labels, processes, parameters



def plot_data():

    plt.figure(figsize=(9, 12))

    [shots, signals, trees, begin, end, low_filter, up_filter, labels, processes, parameters] = get_input()
    # signals = list(reversed(signals))
    # print(processes)
    # print(parameters)

    i = 0
    colors = ['b', 'r', 'g', 'k', 'y']
    n = len(signals)
    m = len(shots)
    # ax = [0]
    # fig=plt.figure()
    for signal in signals:
        tree = trees[i]
        slabel = labels[i]
        process = processes[i]
        parameter = parameters[i]
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
            

            if i == 1:
                if j == 1:
                    plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
                    plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
                    ax1 = plt.subplot(n, 1, i)
                    plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
                    plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
                    if (n-i)&1:
                        plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='off',labelright='on')
                        ax1.yaxis.set_label_position("right") 
                    else:
                        plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='off',labelleft='on',labelright='off')
                    plt.subplots_adjust(wspace =0, hspace =0)
                    
                    plt.ylabel(slabel)
                    plt.xlim([begin, end])
                    
                ax1.plot(t, y, color=color, label=str(shot))
                
                ax1.legend()
                
                
                
                

            # elif i == n:
            #     ax2 = plt.subplot(n, 1, i, sharex=ax1)
            #     ax2.plot(t, y, color=color, label=str(shot))
            #     plt.xlim([begin, end])
            #     ax2.legend()
            
            elif i == n:
                if j == 1:
                    ax2 = plt.subplot(n, 1, i, sharex=ax1)
                    plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
                    plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
                    
                    plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='on',labelleft='on',labelright='off')
                    
                    plt.subplots_adjust(wspace =0, hspace =0)
                    
                    plt.ylabel(slabel)
                    plt.xlabel('time (s)')
                    plt.xlim([begin, end])
                    ax1 = ax2

                ax1.plot(t, y, color=color)
                
                
                
                
                # plt.tick_params(labeltop='off',labelbottom='off',labelleft='off',labelright='off')
                
                
            else:
                if j == 1:
                    ax2 = plt.subplot(n, 1, i, sharex=ax1)
                    plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
                    plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
                    if (n-i)&1:
                        plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='off',labelright='on')
                        ax2.yaxis.set_label_position("right") 
                    else:
                        plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='on',labelright='off')
                    plt.subplots_adjust(wspace =0, hspace =0)
                    
                    plt.ylabel(slabel)
                    plt.xlim([begin, end])
                    ax1 = ax2
                ax1.plot(t, y, color=color)
                
                # if j == m:
                #     ax1 = ax2
                
                
                

                
            # if i==n:
            #     tmp.plot(t, y, color=color, label=str(shot))
            #     tmp.legend()
            #     # tmp.grid()
            #     plt.xlim([begin, end])
            #     ax[i].get_shared_x_axes().join(ax[i], ax[i-1])
            #     ax[i].set_xticklabels([])
            # elif i == 1:
            #     tmp.plot(t, y, color=color)
            #     # tmp.grid()
            #     plt.xlim([begin, end])
            # else:
            #     tmp.plot(t, y, color=color)
            #     tmp.grid()
            #     plt.xlim([begin, end])
            #     ax[i].get_shared_x_axes().join(ax[i], ax[i-1])
            #     ax[i].set_xticklabels([])
                
                    
                
                
                
            # if i==1:
            #     tmp = 1.1*np.max(y)
            #     locationY
            #     locationX = begin+(end-begin)/6*j
            #     plt.text(locationX, locationY, str(shot), color=color, fontsize=12)



    plt.show()










enter = tk.Button(window,text="Enter",command=plot_data)
enter.place(x=110, y=260)

window.mainloop() #进入主循环
