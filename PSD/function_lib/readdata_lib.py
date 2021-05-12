# -*- coding: utf-8 -*-
"""
Module to load MDSplus and read signal from EAST mds data server
chunan@ipp.ac.cn 2016.06.01
"""
# MDSplus lib  should be install independent
import MDSplus
import pylab
import math
import numpy




# --------------------------------------------------------------
# read part time from a shot
def read_signal_fast(tree='east',shot=65020,sig_name='dal2',t_in=[2,4.1],dn=1,i_plot=0):
    """
    read one signal from EAST MDS server with default tree as 'east'
    output: sig, t, unit
    """
    # ---------------------------------------------------------
    # connect EAST database
    east = MDSplus.Connection('202.127.204.12')
    east.openTree(tree,shot)
    # ---------------------------------------------------------
    # read the first 3 points and get time resolution
    t_head=east.get('data(dim_of(\\'+sig_name+')[1:3:1])')
    dt=(t_head[2]-t_head[0])/2
    t_zero=t_head[0]
    # calculate the start and end index of the time array
    i_start=math.floor((t_in[0]-t_zero)/dt)
    i_end=math.floor((t_in[1]-t_zero)/dt)   
    # read signal at given time period    
    sig=east.get('data(\\'+sig_name+')['+str(i_start)+
        ':'+str(i_end)+':'+str(dn)+']')     
    # read time value
    t = east.get('data(dim_of(\\'+ sig_name +'))['+str(i_start)+
        ':'+str(i_end)+':'+str(dn)+']')
    # read signal unit    
    sig_unit=east.get('units(\\' + sig_name+')')

    # ---- convert MDSplus type of data to numpy array type
    sig=numpy.array(sig)
    t=numpy.array(t)
    
    # test read only part time of signal in a shot
    if i_plot == 1:
        pylab.figure()
        pylab.plot(t,sig,'r')
        pylab.xlim([t[0],t[t.shape[0]-1]])
        pylab.legend((sig_name,))
        pylab.xlabel('t(s)')
        pylab.ylabel(sig_name+'('+sig_unit+')')
        #pylab.show()           

    return sig, t, sig_unit 




# -------- author: chunan@ipp.ac.cn 2016/10/05
# read signals in the same tree with same sampling rate and save signals' data as a Dt*Ds matrix
def read_signal_matrix(tree='east',shot=65020,sig_names=['dal1','dal2'],
                       t_in=[2,4.1],dn=1,i_plot=0):
    """
    Read signals from EAST using an array of names
    Output: sig_matrix, t
    """
    # ---- connect EAST database
    east = MDSplus.Connection('202.127.204.12')
    east.openTree(tree,shot)

    # ---- read the first 3 points and get time resolution
    t_head=east.get('data(dim_of(\\'+sig_names[0]+')[1:3:1])')
    dt=(t_head[2]-t_head[0])/2
    t_zero=t_head[0]
    
    # ---- calculate the start and end index of the time array
    i_start=math.floor((t_in[0]-t_zero)/dt)
    i_end=math.floor((t_in[1]-t_zero)/dt)   
    
    # read time value
    t = east.get('data(dim_of(\\'+ sig_names[0] +'))['+str(i_start)+
        ':'+str(i_end)+':'+str(dn)+']')

    # ----read signal at given time period           
    sig_matrix=numpy.zeros([len(t),len(sig_names)])
    for i in range(0,len(sig_names)):
        sig_matrix[:,i]=east.get('data(\\'+sig_names[i]+')['+str(i_start)+
        ':'+str(i_end)+':'+str(dn)+']') 

    # ---- convert MDSplus type of data to numpy array type
    sig_matrix=numpy.array(sig_matrix)
    t=numpy.array(t)
        
    # ---- see read signals
    if i_plot == 1:
        pylab.figure()
        for i in range(0,len(sig_names)):
            pylab.plot(t,sig_matrix[:,i])
            pylab.xlim([t[0],t[t.shape[0]-1]])
            pylab.legend((sig_names[i],))
            pylab.hold('on')
            
        pylab.xlabel('t(s)')
        pylab.legend(sig_names)
        #pylab.show()   
    return sig_matrix, t




i_test = 0
if i_test == 1:
    sig, t, unit = read_signal_fast(i_plot = 1)
    M, t = read_signal_matrix(i_plot = 1)
    pylab.show()
    

    
    
    
