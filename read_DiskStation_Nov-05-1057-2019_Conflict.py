import numpy as np
import matplotlib.pyplot as plt
from MDSplus import *
def fast_read(sig,shot):
    from MDSplus import Connection as CN
    conn=CN('mds.ipp.ac.cn')
    conn.openTree('east',shot)
    x=conn.get('\\'+sig).copy()
    t=conn.get('dim_of('+'\\'+sig+')').copy()
    conn.closeAllTrees()
    ind=np.argmin(np.abs(t-0))
    t=t[ind:]
    x=x[ind:]
    t=np.array(t,dtype=np.float64)
    x=np.array(x,dtype=np.float64)


    return t,x


def read_EAST_TS(shot):
    from MDSplus import Connection as CN
    conn=CN('202.127.204.12')
    conn.openTree('analysis',shot)
    R=conn.get('\\'+'R_coreTS ').copy()
    Z=conn.get('\\'+'Z_coreTS ').copy()
    time=conn.get('dim_of('+'\\'+'Te_maxTS'+')').copy()
    Te=conn.get('\\'+'Te_coreTS ').copy()
    Ne=conn.get('\\'+'ne_coreTS').copy()
    conn.closeAllTrees()


    return R,Z,time,Te,Ne

