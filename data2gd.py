#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module translate the shot data to gongda for ML
caobin@ipp.ac.cn 2020/1/7
"""


import numpy as np
from east_mds import get_data as get
import h5py
V = 2.0431e-4
Pam2P = 4.82e20
V_jhg1 = 3.118e-4
V_dhg1 = 2.919e-4

def data2ml(shot):

    

    Ip = get.data('ipm', shot)
    ne = get.data('dfsdev2', shot, 'pcs_east')
    [t, gauge3] = get.data('JHF1', shot)
    gauge3 = gauge3*4e5
    [t, gauge2] = get.data('PJS204', shot)
    gauge2 = gauge2*4e5
    back2 = np.mean(gauge2[0:10000])
    back3 = np.mean(gauge3[0:10000])
    gauge3 = (back3-gauge3)
    gauge3[gauge3<1e4] = 0
    gauge3 = gauge3*V*Pam2P
    gauge2 = (back2-gauge2)
    gauge2[gauge2<1e4] = 0
    gauge2 = gauge2*V*Pam2P

    totalP_smbi = (t, gauge2+gauge3)


    [t, jhg1] = get.data('jhg1', shot)
    jhg1 = (jhg1-1)*2.5e4
    back = np.mean(jhg1[0:10000])
    jhg1 = back-jhg1
    jhg1[jhg1<3e3] = 0
    jhg1 = jhg1*V_jhg1*Pam2P

    [t, dhg1] = get.data('dhg1', shot)
    dhg1 = (dhg1-1)*2.5e4
    back = np.mean(dhg1[0:10000])
    dhg1 = back-dhg1
    dhg1[dhg1<3e3] = 0
    dhg1 = dhg1*V_jhg1*Pam2P

    totalP_gaspuff = (t, jhg1+dhg1)


    f = h5py.File('/home/ASIPP/caobin/data/'+str(shot)+'.h5', 'w')
    f.create_dataset('density', data=ne)
    f.create_dataset('current', data=Ip)
    f.create_dataset('SMBI injected particles', data=totalP_smbi)
    f.create_dataset('Gas puffing injected particles', data=totalP_gaspuff)
    f.close()

    # np.savez('/home/ASIPP/caobin/data/'+str(shot)+'.npz', ne, Ip, totalP_smbi, totalP_gaspuff)


if __name__ == '__main__':

    shot = input("Input the shot: ")
    shot = int(shot)
    data2ml(shot)