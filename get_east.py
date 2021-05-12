#!/usr/bin/python
# -*-coding: UTF-8 -*-


import numpy as np




def data(signal, shot, tree):
	import sys
	sys.path.append("D:\\Program Files\\MDSplus\\python")
	from MDSplus import Connection as CN
	cn = CN('mds.ipp.ac.cn')
	cn.openTree(tree, shot)
	x = cn.get('\\'+signal).copy()
	t = cn.get('dim_of('+'\\'+signal+')').copy()
	cn.closeAllTrees()
	t = np.array(t, dtype=np.float64)
	x = np.array(x, dtype=np.float64)
	
	return t, x


if __name__ == '__main__':
	
	signal = input("input signal: ")
	shot = input("input shot: ")
	tree = input("input tree: ")
	[t, x] = data(signal, shot, tree)
	np.save("/home/ASIPP/caobin/data/t.npy", t)
	np.save("/home/ASIPP/caobin/data/x.npy", x)