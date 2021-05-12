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




window=tk.Tk() 
window.title("SMBI check") 
window.geometry("300x300") 
window.resizable(width=False, height=False)
l1=tk.Label(window,text="shot", height=1) 
l1.pack() 
l2=tk.Entry(window) 
l2.pack()

def getshot():
    shot=l2.get() 
    shot = int(shot)
    [t_pas104, pas104] = get.data('JHF1', shot, 'east_1')
    pas104 = 1e4*pas104
    if len(t_pas104) > 1000:

        [t_pas105, pas105] = get.data('PAS105', shot, 'east_1')
        pas105 = 1e4*pas105
        [t_pas103, pas103] = get.data('PAS103', shot, 'east_1')
        pas103 = 1e4*pas103
        [t_smbi3, smbi3] = get.data('SMBI3', shot, 'east')
        [t_g105, g105] = get.data('G105', shot, 'east_1')
        g105 = np.exp(1.667*g105-9.333)
        print('SMBI3 ok')

        [t_pjs203, pjs203] = get.data('PJS203', shot, 'east_1')
        pjs203 = 1e4*pjs203
        [t_pjs204, pjs204] = get.data('PJS204', shot, 'east_1')
        pjs204 = 1e4*pjs204
        [t_pjs205, pjs205] = get.data('PJS205', shot, 'east_1')
        pjs205 = 1e4*pjs205
        [t_smbi2, smbi2] = get.data('SMBI2', shot, 'east')
        [t_g103, g103] = get.data('G401', shot, 'east_1')
        g103 = np.exp(1.667*g103-9.333)
        print('SMBI2 ok')

        plt.figure(figsize=(9, 9))

        plt.subplot(4, 2, 1)
        plt.plot(t_pjs204, pjs204)
        plt.title('SMBI2')

        plt.subplot(4, 2, 2)
        plt.plot(t_pas104, pas104)
        plt.title('SMBI3')

        plt.subplot(4, 2, 3)
        plt.plot(t_pjs205, pjs205)
        

        plt.subplot(4, 2, 4)
        plt.plot(t_pas105, pas105)
        

        plt.subplot(4, 2, 5)
        plt.plot(t_smbi2, smbi2, color='red')
        

        plt.subplot(4, 2, 6)
        plt.plot(t_smbi3, smbi3, color='red')
        

        plt.subplot(4, 2, 7)
        plt.plot(t_g103, g103)
        

        plt.subplot(4, 2, 8)
        plt.plot(t_g105, g105)
        

        plt.show()
        
        

    else:
        l3.delete('1.0','end')
        l3.insert('end', 'Error: No data')





tk.Button(window,text="Enter",command=getshot).pack() #command绑定获取文本框内容方法
l3 = tk.Text(window, height=1)
l3.pack()
window.mainloop() #进入主循环
