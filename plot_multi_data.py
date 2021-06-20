#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module plot the multiple east data 
caobin@ipp.ac.cn 2021/5/26
"""



import matplotlib.pyplot as plt
import numpy as np
import MDSplus as mds


if __name__ == '__main__':

    signal = input('Input the signal: ')
    shot = input('Input the shot: ')
    shot = int(shot)
    tree = input('Input the tree: ')

    begin_time = input('Input the begin_time: ')
    begin_time = float(begin_time)
    end_time = input('Input the end_time: ')
    end_time = float(end_time)
    
    n = input('input the number of changes: ')
    n = int(n)
    nlist = range(1, n+1)

    cn = mds.Connection('mds.ipp.ac.cn')
    cn.openTree(tree, shot)
    signal_name = signal+'1'
    t =  cn.get('dim_of('+'\\'+signal_name+')').copy()
    index = np.where((t>=begin_time)&(t<=end_time))
    t = t[index]
    data = np.zeros([n, len(t)], dtype=np.float64)
    for i in nlist:
        signal_name = signal+str(i)
        tmp = cn.get('\\'+signal_name).copy()
        tmp = tmp[index]
        data[i-1, :] = np.array(tmp, dtype=np.float64)

    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in' 
    plt.subplots(figsize=(8,8),dpi=100)
    cmap = plt.cm.rainbow
    CS = plt.pcolormesh(t, nlist, data, cmap='jet')
    cbar = plt.colorbar(CS)


    plt.tight_layout()
    vmax = 0.5*np.max(data)
    # plt.clim(0,vmax)
    plt.show()