'''
Description: 
Author: caobin
Date: 2021-06-25 
Github: https://github.com/bcao19
LastEditors: caobin
LastEditTime: 2021-06-25
'''
#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module for math 
caobin@ipp.ac.cn 2021/6/25
"""

import numpy as np


def find_min_idx(x):
    location = np.where(x == np.min(x))
    return location


def find_max_idx(x):
    location = np.where(x == np.max(x))
    return location