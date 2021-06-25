'''
Description: 
Author: caobin
Date: 2021-06-22 
Github: https://github.com/bcao19
LastEditors: caobin
LastEditTime: 2021-06-22
'''
#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module get the rho from efit or efitrt
type=1 rho from psi, type=2 rho from sqrt(rho), type=3 rho from r/a
caobin@ipp.ac.cn 2021/6/22
"""

import numpy as np
from east_mds import get_data as get


def read(shot, time, efit='efit_east'):
    t_efit = get.data1('gtime', shot, efit)
    t_efit = abs(t_efit-time)
    index_efit = np.argmin(t_efit)

    r_psi = get.data1('r', shot, efit)
    z_psi = get.data1('z', shot, efit)

    ssimag = get.data1('ssimag', shot, efit)
    ssimag = ssimag[index_efit]

    psi = get.data1('psirz', shot, efit)
    psi = psi[index_efit, :, :]-ssimag

    ssibry = get.data1('ssibry', shot, efit)
    ssibry = ssibry[index_efit]-ssimag

    rho = psi/ssibry

    return r_psi, z_psi, rho




