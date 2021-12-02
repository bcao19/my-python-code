'''
Author       : caobin
Date         : 2021-09-27 14:32:27
LastEditors  : caobin
LastEditTime : 2021-09-27 15:40:51
FilePath     : \my-python-code\get_DFPI.py
read DFPI injected paticles
'''


from tkinter.constants import X


def read(shot, timerange):
    from east_mds import get_data as get
    import numpy as np
    [t, x] = get.data('PDS1_2', shot, tree='east_1', timerange=timerange)
    
    background = np.mean(x[0:100])
    x = background-x
    x = 4e-4*4.82e20*x

    return t,x

