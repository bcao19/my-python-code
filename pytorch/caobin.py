'''
Author       : caobin
Date         : 2022-08-09 15:34:14
LastEditors  : caobin
LastEditTime : 2022-08-17 08:28:58
FilePath     : \my-python-code\pytorch\caobin.py
'''

import math
import numpy as np
import torch
from torch import nn
from pytorch import d2l 

import os
os.environ["KMP_DUPLICATE_LIB_OK"]  =  "TRUE"




def try_gpu(i=0):  #@save
    """如果存在，则返回gpu(i)，否则返回cpu()"""
    if torch.cuda.device_count() >= i + 1:
        return torch.device(f'cuda:{i}')
    return torch.device('cpu')

def try_all_gpus():  #@save
    """返回所有可用的GPU，如果没有GPU，则返回[cpu(),]"""
    devices = [torch.device(f'cuda:{i}')
             for i in range(torch.cuda.device_count())]
    return devices if devices else [torch.device('cpu')]