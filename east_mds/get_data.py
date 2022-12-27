'''
Description: 
Author: caobin
Date: 2021-07-26 21:09:30
Github: https://github.com/bcao19
LastEditors: caobin
LastEditTime: 2021-07-26 23:19:23
'''
'''
Author       : caobin
Date         : 2021-05-12 09:40:00
LastEditors: caobin
LastEditTime: 2021-07-20 15:04:29
FilePath     : \my-python-code\east_mds\get_data.py
'''
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
import scipy.signal as sig


def data(signal, shot, **kw):
	
	if 'tree' in kw:
		tree = kw['tree']
	else:
		tree = 'east'

	cn = mds.Connection('202.127.204.12')
	cn.openTree(tree, shot)
	x = cn.get('\\'+signal).copy()
	t = cn.get('dim_of('+'\\'+signal+')').copy()
	cn.closeAllTrees()
	t = np.array(t, dtype=np.float64)
	x = np.array(x, dtype=np.float64)


	if 'timerange' in kw:
		timerange = kw['timerange']
		index = np.where((t>=np.min(timerange))&(t<=np.max(timerange)))
		t = t[index]
		x = x[index]

	judge = signal[0:2]
	if judge == "G1":
		temp = x
		x = 10**(temp*1.667-9.333)

	elif judge == "PA" or judge == "PJ":
		temp = x
		x = 2e3*temp
		
	elif judge == "PP" or judge == "PD":
		temp = x
		x = 2e4*temp



	if 'medfilt' in kw:
		n = kw['medfilt']
		x = sig.medfilt(x, n)


	if 'move' in kw:
		move = kw['move']
		t = t-move


	if 'smooth' in kw:
		win = kw['smooth'][0]
		k = kw['smooth'][1]
		x = sig.savgol_filter(x, win, k)

	if 'log' in kw:
		if kw['log'] == 10:
			x = np.log10(x)
		elif kw['log'] == 2:
			x = np.log2(x)
		else:
			x = np.log(x)

	if 'zoom' in kw:
		n = kw['zoom']
		x = n*x


	return t, x


def data1(signal, shot, tree='east'):
	
	cn = mds.Connection('mds.ipp.ac.cn')
	cn.openTree(tree, shot)
	x = cn.get('\\'+signal).copy()
	
	cn.closeAllTrees()
	
	x = np.array(x, dtype=np.float64)
	
	return x