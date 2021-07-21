'''
Author       : caobin
Date         : 2021-07-21 14:48:54
LastEditors  : caobin
LastEditTime : 2021-07-21 14:59:36
FilePath     : \my-python-code\get_test.py
'''
'''
'''

from east_mds import get_data as get

def read(shot, timerange=[0, 10]): 
    [t, x] = get.data('G107', shot, timerange=timerange)


    return t, x