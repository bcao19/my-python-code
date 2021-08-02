'''
Description: 
Author: caobin
Date: 2021-07-26 22:01:31
Github: https://github.com/bcao19
LastEditors: caobin
LastEditTime: 2021-08-02 09:25:40
'''
'''
Description: 
Author: caobin
Date: 2021-07-26 22:01:31
Github: https://github.com/bcao19
LastEditors: caobin
LastEditTime: 2021-07-26 22:01:31
'''

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
window.geometry("1375x300") #设置窗口尺寸
names = locals()
names['shot0'] = tk.Label(window,text="shot", height=1) #标签
names['shot0'].place(x=20, y=10) #指定包管理器放置组件


names['shot1'] = tk.Entry()
names['shot1'].place(x=10, y=35, width=50)
    

names['signal10'] = tk.Label(window,text="signal", height=1) #标签
names['signal10'].place(x=100, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['signal1'+str(i)] = tk.Entry()
    names['signal1'+str(i)].place(x=80, y=10+25*i, width=80)



names['tree10'] = tk.Label(window,text="tree", height=1) #标签
names['tree10'].place(x=200, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['tree1'+str(i)] = tk.Entry()
    names['tree1'+str(i)].place(x=180, y=10+25*i, width=80)



names['label10'] = tk.Label(window,text="label", height=1) #标签
names['label10'].place(x=300, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['label1'+str(i)] = tk.Entry()
    names['label1'+str(i)].place(x=280, y=10+25*i, width=80)

names['zoom10'] = tk.Label(window,text="zoom", height=1) #标签
names['zoom10'].place(x=400, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['zoom1'+str(i)] = tk.Entry()
    names['zoom1'+str(i)].place(x=380, y=10+25*i, width=80)



names['signal20'] = tk.Label(window,text="signal", height=1) #标签
names['signal20'].place(x=500, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['signal2'+str(i)] = tk.Entry()
    names['signal2'+str(i)].place(x=480, y=10+25*i, width=80)



names['tree20'] = tk.Label(window,text="tree", height=1) #标签
names['tree20'].place(x=600, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['tree2'+str(i)] = tk.Entry()
    names['tree2'+str(i)].place(x=580, y=10+25*i, width=80)



names['label20'] = tk.Label(window,text="label", height=1) #标签
names['label20'].place(x=700, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['label2'+str(i)] = tk.Entry()
    names['label2'+str(i)].place(x=680, y=10+25*i, width=80)

names['zoom20'] = tk.Label(window,text="zoom", height=1) #标签
names['zoom20'].place(x=800, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['zoom2'+str(i)] = tk.Entry()
    names['zoom2'+str(i)].place(x=780, y=10+25*i, width=80)

    

names['signal30'] = tk.Label(window,text="signal", height=1) #标签
names['signal30'].place(x=900, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['signal3'+str(i)] = tk.Entry()
    names['signal3'+str(i)].place(x=880, y=10+25*i, width=80)



names['tree30'] = tk.Label(window,text="tree", height=1) #标签
names['tree30'].place(x=1000, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['tree3'+str(i)] = tk.Entry()
    names['tree3'+str(i)].place(x=980, y=10+25*i, width=80)



names['label30'] = tk.Label(window,text="label", height=1) #标签
names['label30'].place(x=1100, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['label3'+str(i)] = tk.Entry()
    names['label3'+str(i)].place(x=1080, y=10+25*i, width=80)

names['zoom30'] = tk.Label(window,text="zoom", height=1) #标签
names['zoom30'].place(x=1200, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['zoom3'+str(i)] = tk.Entry()
    names['zoom3'+str(i)].place(x=1180, y=10+25*i, width=80)

names['unit0'] = tk.Label(window,text="unit", height=1) #标签
names['unit0'].place(x=1300, y=10) #指定包管理器放置组件

for i in range(1, 8):
    names['unit'+str(i)] = tk.Entry()
    names['unit'+str(i)].place(x=1280, y=10+25*i, width=80)





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
    
    signals1 = []
    trees1 = []
    labels1 = []
    zooms1 = []
    signals2 = []
    trees2 = []
    labels2 = []
    zooms2 = []
    signals3 = []
    trees3 = []
    labels3 = []
    zooms3 = []
    units = []

    


    shot = names['shot1'].get()
        
    if len(shot)>0:
        shot = int(shot)
    else:
        from MDSplus import Connection as CN
        cn = CN('mds.ipp.ac.cn')
        shot = cn.get("current_shot('east')")
        shot = int(shot)


    for i in range(1, 8):
        signal1 = names['signal1'+str(i)].get()
        tree1 = names['tree1'+str(i)].get()
        label1 = names['label1'+str(i)].get()
        zoom1 = names['zoom1'+str(i)].get()
        signal2 = names['signal2'+str(i)].get()
        tree2 = names['tree2'+str(i)].get()
        label2 = names['label2'+str(i)].get()
        zoom2 = names['zoom2'+str(i)].get()
        signal3 = names['signal3'+str(i)].get()
        tree3 = names['tree3'+str(i)].get()
        label3 = names['label3'+str(i)].get()
        zoom3 = names['zoom3'+str(i)].get()
        unit = names['unit'+str(i)].get()

        if len(signal1)>0:
            signals1.append(signal1)
            if len(tree1) == 0:
                trees1.append('east_1')
            else:
                trees1.append(tree1)

            if len(label1) == 0:
                labels1.append(signal1)
            else:
                labels1.append(label1)

            if len(zoom1) == 0:
                zooms1.append(1)
            else:
                zooms1.append(float(zoom1))

            if len(signal2)>0:
                signals2.append(signal2)
                if len(tree2) == 0:
                    trees2.append('east_1')
                else:
                    trees2.append(tree2)

                if len(label2) == 0:
                    labels2.append(signal2)
                else:
                    labels2.append(label2)

                if len(zoom2) == 0:
                    zooms2.append(1)
                else:
                    zooms2.append(float(zoom2))
            else:
                signals2.append('0')
                trees2.append('0')
                labels2.append('0')
                zooms2.append(0)

            

            if len(signal3)>0:
                signals3.append(signal3)
                if len(tree3) == 0:
                    trees3.append('east_1')
                else:
                    trees3.append(tree3)

                if len(label3) == 0:
                    labels3.append(signal3)
                else:
                    labels3.append(label3)
                
                if len(zoom3) == 0:
                    zooms3.append(1)
                else:
                    zooms3.append(float(zoom3))
            else:
                signals3.append('0')
                trees3.append('0')
                labels3.append('0')
                zooms3.append(0)
            
            if len(unit)>0:
                units.append(unit)
            else:
                units.append('0')



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
    

    return shot, signals1, trees1, labels1, zooms1, signals2, trees2, labels2, zooms2, signals3, trees3, labels3, zooms3, units, begin_time, end_time, low_frequency, up_frequency



def plot_data():

    plt.figure(figsize=(9, 12))
    plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内

    [shot, signals1, trees1, labels1, zooms1, signals2, trees2, labels2, zooms2, signals3, trees3, labels3, zooms3, units, begin, end, low_filter, up_filter] = get_input()

    plt.title(str(shot))
    
    # signals = list(reversed(signals))
    # print(processes)
    # print(parameters)

    i = 0
    colors = ['b', 'r', 'g']
    n = len(signals1)

    # ax = [0]
    # fig=plt.figure()
    for signal in signals1:
        tree = trees1[i]
        slabel = labels1[i]
        zoom = zooms1[i]
        signal2 = signals2[i]
        tree2 = trees2[i]
        slabel2 = labels2[i]
        zoom2 = zooms2[i]
        signal3 = signals3[i]
        tree3 = trees3[i]
        slabel3 = labels3[i]
        zoom3 = zooms3[i]
        unit = units[i]
        
        i = i+1
        
        color = colors[0]
        # print(signal)

        [t, y] = get.data(signal, shot, tree=tree, timerange=[begin, end], zoom=zoom)


            

            # if shot == 98346:
            #     temp = np.array(t)
            #     temp = temp-7
            #     t = temp

            # if shot == 98351:
            #     temp =np.array(t)
            #     temp = temp-5.5
            #     t = temp
            
            # index = np.where((t>=begin)&(t<=end))            
            # t = t[index]
            # y = y[index]


        if up_filter != 0:
            fs = 100/(t[100]-t[0])
            fs = int(fs)
            if low_filter == 0:
                y = filter.high_pass(y, up_filter, fs)
            elif up_filter >= 0.5*fs:
                y = filter.low_pass(y, low_filter, fs)
            else:
                y = filter.band_stop(y, low_filter, up_filter, fs)
        
        
        
        

        
        
        if i == 1:

            plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
            plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
            ax1 = plt.subplot(n, 1, i)
                
            plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
            plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
            plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='off',labelleft='on',labelbottom=False)
                # if (n-i)&1:
                #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='off',labelright='on')
                #     ax1.yaxis.set_label_position("right") 
                # else:
                #     plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='off',labelleft='on',labelright='off')
            if n == 1:
                plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='on',labelleft='on',labelright='off')
            plt.subplots_adjust(wspace =0, hspace =0.03*n)
            ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
            if unit != '0':
                plt.ylabel(unit)
            plt.xlim([begin, end])
                
            ax1.plot(t, y, color=color, label=slabel)
            if signal2 != '0':
                print(signal2)
                [t2, y2] = get.data(signal2, shot, tree=tree2, timerange=[begin, end], zoom=zoom2)
                ax1.plot(t2, y2, color=colors[1], label=slabel2)
            if signal3 != '0':
                [t3, y3] = get.data(signal3, shot, tree=tree3, timerange=[begin, end], zoom=zoom3)
                ax1.plot(t3, y3, color=colors[2], label=slabel3)
            
            ax1.legend()



        elif i == n:
            
            ax2 = plt.subplot(n, 1, i, sharex=ax1)
                
            plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
            plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
                
            plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='on',labelleft='on',labelright='off')
                
            plt.subplots_adjust(wspace =0, hspace =0.03*n)
            ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
            if unit != '0':
                plt.ylabel(unit)
            plt.xlabel('time (s)')
            plt.xlim([begin, end])
            ax1 = ax2

            ax1.plot(t, y, color=color, label=slabel)
            if signal2 != '0':
                [t2, y2] = get.data(signal2, shot, tree=tree2, timerange=[begin, end], zoom=zoom2)
                ax1.plot(t2, y2, color=colors[1], label=slabel2)
            if signal3 != '0':
                [t3, y3] = get.data(signal3, shot, tree=tree3, timerange=[begin, end], zoom=zoom3)
                ax1.plot(t3, y3, color=colors[2], label=slabel3)
            ax1.legend()
            
            
            
            
            # plt.tick_params(labeltop='off',labelbottom='off',labelleft='off',labelright='off')
            
            
            
            

        # elif i == n:
        #     ax2 = plt.subplot(n, 1, i, sharex=ax1)
        #     ax2.plot(t, y, color=color, label=str(shot))
        #     plt.xlim([begin, end])
        #     ax2.legend()
        
        
            
            
        else:

            ax2 = plt.subplot(n, 1, i, sharex=ax1)
                
            plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
            plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
                # if (n-i)&1:
                #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='off',labelright='on')
                #     ax2.yaxis.set_label_position("right") 
                # else:
                #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='on',labelright='off')
            plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='on',labelbottom=False)
            plt.subplots_adjust(wspace =0, hspace =0.03*n)
            ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
            if unit != '0':
                plt.ylabel(unit)
            plt.xlim([begin, end])
            ax1 = ax2
            ax1.plot(t, y, color=color, label=slabel)
            if signal2 != '0':
                [t2, y2] = get.data(signal2, shot, tree=tree2, timerange=[begin, end], zoom=zoom2)
                ax1.plot(t2, y2, color=colors[1], label=slabel2)
            if signal3 != '0':
                [t3, y3] = get.data(signal3, shot, tree=tree3, timerange=[begin, end], zoom=zoom3)
                ax1.plot(t3, y3, color=colors[2], label=slabel3)
            ax1.legend()
            
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

    # i = 0
    # n = len(signals2)
    
    # for signal in signals2:
    #     tree = trees2[i]
    #     slabel = labels2[i]
            
    #     i = i+1
    #     plt.subplot(n, 1, i)
    #     if signal != '0':
            
            
            
    #         color = colors[1]

            
    #         [t, y] = get.data(signal, shot, tree=tree, timerange=[begin, end], zoom=zoom)


                

    #             # if shot == 98346:
    #             #     temp = np.array(t)
    #             #     temp = temp-7
    #             #     t = temp

    #             # if shot == 98351:
    #             #     temp =np.array(t)
    #             #     temp = temp-5.5
    #             #     t = temp
                
    #             # index = np.where((t>=begin)&(t<=end))            
    #             # t = t[index]
    #             # y = y[index]


    #         if up_filter != 0:
    #             fs = 100/(t[100]-t[0])
    #             fs = int(fs)
    #             if low_filter == 0:
    #                 y = filter.high_pass(y, up_filter, fs)
    #             elif up_filter >= 0.5*fs:
    #                 y = filter.low_pass(y, low_filter, fs)
    #             else:
    #                 y = filter.band_stop(y, low_filter, up_filter, fs)
            
            
    #         judge = signal[0:2]
    #         if judge == "G1":
    #             temp = np.array(y)
    #             temp = 10**(temp*1.667-9.333)
    #             y = list(temp)
    #         elif judge == "PA" or judge == "PJ":
    #             temp = np.array(y)
    #             temp = 2e3*temp
    #             y = list(temp)
    #         elif judge == "PP" or judge == "PD":
    #             temp = np.array(y)
    #             temp = 2e4*temp
    #             y = list(temp)
            

            
            
    #         if i == 1:

    #             plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    #             plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
    #             ax1 = plt.subplot(n, 1, i)
                    
    #             plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    #             plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
    #             plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='off',labelleft='on',labelright='off')
    #                 # if (n-i)&1:
    #                 #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='off',labelright='on')
    #                 #     ax1.yaxis.set_label_position("right") 
    #                 # else:
    #                 #     plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='off',labelleft='on',labelright='off')
    #             if n == 1:
    #                 plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='on',labelleft='on',labelright='off')
    #             plt.subplots_adjust(wspace =0, hspace =0.03*n)
    #             ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    #             # plt.ylabel(slabel)
    #                 # plt.xlim([begin, end])
                    
    #             ax1.plot(t, y, color=color, label=slabel)
                
    #             ax1.legend()



    #         elif i == n:
                
    #             ax2 = plt.subplot(n, 1, i, sharex=ax1)
                    
    #             plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    #             plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
                    
    #             plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='on',labelleft='on',labelright='off')
                    
    #             plt.subplots_adjust(wspace =0, hspace =0.03*n)
    #             ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    #             # plt.ylabel(slabel)
    #             plt.xlabel('time (s)')
    #                 # plt.xlim([begin, end])
    #             ax1 = ax2

    #             ax1.plot(t, y, color=color, label=slabel)
    #             ax1.legend()
                
                
                
                
    #             # plt.tick_params(labeltop='off',labelbottom='off',labelleft='off',labelright='off')
                
                
                
                

    #         # elif i == n:
    #         #     ax2 = plt.subplot(n, 1, i, sharex=ax1)
    #         #     ax2.plot(t, y, color=color, label=str(shot))
    #         #     plt.xlim([begin, end])
    #         #     ax2.legend()
            
            
                
                
    #         else:

    #             ax2 = plt.subplot(n, 1, i, sharex=ax1)
                    
    #             plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    #             plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
    #                 # if (n-i)&1:
    #                 #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='off',labelright='on')
    #                 #     ax2.yaxis.set_label_position("right") 
    #                 # else:
    #                 #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='on',labelright='off')
    #             plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='on',labelright='off')
    #             plt.subplots_adjust(wspace =0, hspace =0.03*n)
    #             ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    #             # plt.ylabel(slabel)
    #                 # plt.xlim([begin, end])
    #             ax1 = ax2
    #             ax1.plot(t, y, color=color, label=slabel)
    #             ax1.legend()

    # i = 0
    # n = len(signals3)
    

    # for signal in signals3:
    #     tree = trees3[i]
    #     slabel = labels3[i]
            
    #     i = i+1
    #     plt.subplot(n, 1, i)
    #     if signal != '0':
            
            
    #         color = colors[2]

                
    #         [t, y] = get.data(signal, shot, tree=tree, timerange=[begin, end], zoom=zoom)


                

    #             # if shot == 98346:
    #             #     temp = np.array(t)
    #             #     temp = temp-7
    #             #     t = temp

    #             # if shot == 98351:
    #             #     temp =np.array(t)
    #             #     temp = temp-5.5
    #             #     t = temp
                
    #             # index = np.where((t>=begin)&(t<=end))            
    #             # t = t[index]
    #             # y = y[index]


    #         if up_filter != 0:
    #             fs = 100/(t[100]-t[0])
    #             fs = int(fs)
    #             if low_filter == 0:
    #                 y = filter.high_pass(y, up_filter, fs)
    #             elif up_filter >= 0.5*fs:
    #                 y = filter.low_pass(y, low_filter, fs)
    #             else:
    #                 y = filter.band_stop(y, low_filter, up_filter, fs)
            
            
    #         judge = signal[0:2]
    #         if judge == "G1":
    #             temp = np.array(y)
    #             temp = 10**(temp*1.667-9.333)
    #             y = list(temp)
    #         elif judge == "PA" or judge == "PJ":
    #             temp = np.array(y)
    #             temp = 2e3*temp
    #             y = list(temp)
    #         elif judge == "PP" or judge == "PD":
    #             temp = np.array(y)
    #             temp = 2e4*temp
    #             y = list(temp)
            

            
            
    #         if i == 1:

    #             plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    #             plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
    #             ax1 = plt.subplot(n, 1, i)
                    
    #             plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    #             plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
    #             plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='off',labelleft='on',labelright='off')
    #                 # if (n-i)&1:
    #                 #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='off',labelright='on')
    #                 #     ax1.yaxis.set_label_position("right") 
    #                 # else:
    #                 #     plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='off',labelleft='on',labelright='off')
    #             if n == 1:
    #                 plt.tick_params(top='on',bottom='on',left='on',right='on', labeltop='off',labelbottom='on',labelleft='on',labelright='off')
    #             plt.subplots_adjust(wspace =0, hspace =0.03*n)
    #             ax1.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    #             # plt.ylabel(slabel)
    #                 # plt.xlim([begin, end])
                    
    #             ax1.plot(t, y, color=color, label=slabel)
                
    #             ax1.legend()



    #         elif i == n:
                
    #             ax2 = plt.subplot(n, 1, i, sharex=ax1)
                    
    #             plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    #             plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
                    
    #             plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='on',labelleft='on',labelright='off')
                    
    #             plt.subplots_adjust(wspace =0, hspace =0.03*n)
    #             ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    #             # plt.ylabel(slabel)
    #             plt.xlabel('time (s)')
    #                 # plt.xlim([begin, end])
    #             ax1 = ax2

    #             ax1.plot(t, y, color=color, label=slabel)
    #             ax1.legend()
                
                
                
                
    #             # plt.tick_params(labeltop='off',labelbottom='off',labelleft='off',labelright='off')
                
                
                
                

    #         # elif i == n:
    #         #     ax2 = plt.subplot(n, 1, i, sharex=ax1)
    #         #     ax2.plot(t, y, color=color, label=str(shot))
    #         #     plt.xlim([begin, end])
    #         #     ax2.legend()
            
            
                
                
    #         else:

    #             ax2 = plt.subplot(n, 1, i, sharex=ax1)
                    
    #             plt.rcParams['xtick.direction'] = 'in'#将x周的刻度线方向设置向内
    #             plt.rcParams['ytick.direction'] = 'in'#将y轴的刻度方向设置向内
    #                 # if (n-i)&1:
    #                 #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='off',labelright='on')
    #                 #     ax2.yaxis.set_label_position("right") 
    #                 # else:
    #                 #     plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='on',labelright='off')
    #             plt.tick_params(top='on',bottom='on',left='on',right='on',labeltop='off',labelbottom='off',labelleft='on',labelright='off')
    #             plt.subplots_adjust(wspace =0, hspace =0.03*n)
    #             ax2.ticklabel_format(style='sci', scilimits=(-1,2), axis='y')
    #             plt.ylabel(slabel)
    #                 # plt.xlim([begin, end])
    #             ax1 = ax2
    #             ax1.plot(t, y, color=color, label=slabel)
    #             ax1.legend()

    



    plt.show()










enter = tk.Button(window,text="Enter",command=plot_data)
enter.place(x=110, y=260)

window.mainloop() #进入主循环
