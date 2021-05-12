#!/home/ASIPP/caobin/anaconda3/bin/python
# -*-coding: UTF-8 -*-


"""
this module will get the data from MDSplus and tranlate to array
caobin@ipp.ac.cn 2019/12/30
"""

__author__ = 'caobin'

import MDSplus as mds
import numpy as np
import matplotlib.pyplot as plt


def data(signal, shot, tree='east'):
	
	cn = mds.Connection('mds.ipp.ac.cn')
	cn.openTree(tree, shot)
	x = cn.get('\\'+signal).copy()
	t = cn.get('dim_of('+'\\'+signal+')').copy()
	cn.closeAllTrees()
	t = np.array(t, dtype=np.float64)
	x = np.array(x, dtype=np.float64)
	
	return t, x
