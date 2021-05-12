#!/usr/bin/env python
""" 
  GEQDSK EXTRACTER FROM MDS-PLUS (By Hyunsun)

History:
  - modified that the output geqdsk can be read by any standard geqdsk reader such
    as efitviewer                                             - YMJ at Jan/10/2013

Example)
  run(shot,time_i,time_f);
"""
#------------------------------------------------------------------------------------#
# Module to plot CES and Thomson data from MDSPLUS in KSTAR is added by Hyungho Lee
#------------------------------------------------------------------------------------#
import ctypes as _C
from MDSplus import Connection
from MDSplus._mdsshr import _load_library, MdsException 

ConnectToMds=_load_library('MdsIpShr').ConnectToMds
ConnectToMds.argtypes=[_C.c_char_p]
DisconnectFromMds = _load_library('MdsIpShr').DisconnectFromMds
DisconnectFromMds.argtypes = [_C.c_int]

class _Connection( Connection):
    """
    Updating 'Connection' class in 'MDSplus' to manange the connection to the server
    (1) hanging off the connection when termination
    (2) retry the connection by 'reconnect' method
    Written by D. K. Oh
    Last Modification : Aug 2012
    """
    def __del__(self):
        self.closeConnection()
        
    def closeConnection(self):
        if self.socket != -1:
             if DisconnectFromMds(self.socket) == 0: 
                raise Exception, "Error in disconnection"
             else:
                self.socket = -1
                
    def reconnect(self):
        if self.hostspec == None:
             raise MdsException, "Error: no host specified"
        else:
             if self.socket != -1:
                print self.socket
                try:
                    self.closeConnection()
                except:
                    raise Exception, "Error in resetting connection to %s" %(self.hostspec,)
             self.socket = ConnectToMds(self.hostspec)
             if self.socket == -1:
                raise Exception, "Error connecting to %s" %(self.hostspec,)   

class MDS(object):
    """
    Implementation of a connection to the MDSplus tree based on the class mds by Y. M. Jeon
    Written by D. K. Oh
    Last modification : Aug 2012
    """
    __DefaultTree = "KSTAR"
    __DefaultServer = "172.17.250.100:8005"

    def __init__(self, shot=None, tree =__DefaultTree, server=__DefaultServer):
        try:                    
            self.alist = {"tree":None, "shot":None, "server":None}
            self.__mds__ = _Connection(server)
            if shot is not None:
                self.open(shot, tree)
        except MdsException:
            raise MdsException, "Error in the connection %s" %(server)
        except:
            raise Exception, " Unknown error in the connection %s" %(server)
        else:
            self.alist = {"tree":tree, "shot":shot, "server":server}
            
    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        self.disconnect()
        
    def reset(self, shot=None, tree=None, server=__DefaultServer):
        if tree is None:
            tree = self.alist["tree"]
        if shot is None:
            shot = self.alist["shot"]
        
        self.alist = {"tree":tree, "shot":shot, "server":server}
        alist = self.alist
        __mds = self.__mds__ 
        __mds.hostspec = alist["server"]
        __mds.reconnect()
        if (shot is not None) and (tree is not None):
            self.open(tree, shot)

    def open(self, shot, tree =__DefaultTree):
        if shot is None:
            shot = self.alist["shot"]
        if shot is None:
            self.alist["tree"] = None
            self.alist["shot"] = None
            raise MdsException, "Error in open : shot number is not specified"
        else:    
            self.close( self.alist["shot"], self.alist["tree"])
            try:
                self.__mds__.openTree(tree, shot)
            except:
                self.alist["tree"] = None
                self.alist["shot"] = None
                raise MdsException, "Error in open : unknown error"    
            else:
                self.alist["tree"] = tree
                self.alist["shot"] = shot
                return self.__mds__

    def close(self, shot=None, tree=None): 
        if tree is None:
            tree = self.alist["tree"]
        if shot is None:
            shot = self.alist["shot"]
        if (shot is not None) and (tree is not None):
            try:
                self.__mds__.closeTree(tree, shot)
            except:
                raise MdsException, "Error in close : unknown error"
            else:
                self.alist["shot"] = None
                self.alist["tree"] = None

    def disconnect(self): self.__mds__.closeConnection()
        
    def get_T0(self):
        try:
            ret_str = self.__mds__.get('\T0_STR').data()
        except:
            ret_str = None            
            raise MdsException, "Error in get"
        return ret_str

    def get_sig(self, sigstr):
        try:
            t = self.__mds__.get('dim_of(%s)' %(sigstr)).data();
            v = self.__mds__.get(sigstr).data();
        except:
            t = numpy.ndarray([])
            v = numpy.ndarray([])             
            raise MdsException, "Error in get"
        return t,v;

    def get_sig_data(self, sigstr):
        try:
            v = self.__mds__.get(sigstr).data();
        except:
            v = numpy.ndarray([])
            raise MdsException, "Error in get"
        return v;


#-------------------------------------------------------------------------------#
def write_profile(fp,data2):
    i=0;
    for data in data2 :
          fp.write(str("%16.9e"%data));
          i=i+1;
          if(i==5):
                fp.write(str("\n"));
                i=0;
    if(i>0): fp.write(str("\n"));         

    return 

#--------------------------------------------------------------------------------#
def run(shot,time_i,time_f,t_interval=0.1, treename='kstar'):
#def run(shot, treename='kstar'):
    """ """
    import os, sys
    import time as time_module
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import interpolate
    from scipy.interpolate import interp1d
    from scipy.interpolate import interp2d
    from scipy.interpolate import Rbf
    from scipy.interpolate import RectBivariateSpline
    from matplotlib.mlab import griddata

    tcesR_prefix='\\ces_rt';
    cesti_prefix='\\ces_ti';
    cesvt_prefix='\\ces_vt';
    CESTiPARAMETERS=[];
    TORRADIUS=[];
    CESVtPARAMETERS=[];
    for i in range(1,33):
        tmp_idx=str(i).zfill(2);
        CESTiPARAMETERS.append(cesti_prefix+tmp_idx);
        CESVtPARAMETERS.append(cesvt_prefix+tmp_idx);
        TORRADIUS.append(tcesR_prefix+tmp_idx);
    
    cesti=[];
    cesvt=[];
    tcesR=[];
    cestime=[];
    geqdsk=[];
    
    # get all data for PARAMETERS
    ces_plot_on=1;
    with MDS(server="172.17.100.200:8005") as mds:
       try:
           #eq=mds.open(shot=shot, tree=treename);
           eq=mds.open(shot=shot, tree='kstar');
       except: 
           print "Error #1"
       else:
           try:
               print mds.alist
               for signame in CESTiPARAMETERS:
                   print 'reading ...',signame
                   temp = eq.get(signame).data();
                   temp_time=eq.get('dim_of(%s)' %(signame)).data();
                   cestime=temp_time;
                   cesti.append(temp)
                   #print cesti[:][0];
                   #geqdsk.append(temp); 
               for signame in CESVtPARAMETERS:
                   print 'reading ...',signame
                   temp = eq.get(signame).data();
                   #temp_time=eq.get('dim_of(%s)' %(signame)).data();
                   #cestime=temp_time;
                   cesvt.append(temp)
               for signame in TORRADIUS:
                   print 'reading ...',signame
                   temp = eq.get(signame).data();
                   #temp_time=eq.get('dim_of(%s)' %(signame)).data();
                   tcesR.append(temp);
           except:
               print "Cannot reading the signal\n Quit the program";          
               #sys.exit(0);
               #ces_plot_on=0;
           else:
               print "END of reading"
    mds.close();


    #TSR_prefix='\\ces_rt';
    #cesti_prefix='\\ces_ti';
    #cesvt_prefix='\\ces_vt';
    TSTePARAMETERS=[];
    TSRADIUS=[];
    TSNePARAMETERS=[];
    for i in range(1,28):
        if (i < 13):
           tmp_idx=str(i);
           Te_node='\\TS_CORE'+tmp_idx+':CORE'+tmp_idx+'_TE'
           Ne_node='\\TS_CORE'+tmp_idx+':CORE'+tmp_idx+'_NE'
           R_node='\\TS_CORE'+tmp_idx+':CORE'+tmp_idx+'_POS'
           TSTePARAMETERS.append(Te_node);
           TSNePARAMETERS.append(Ne_node);
           TSRADIUS.append(R_node);
        else:
           tmp_idx=str(i-12);
           Te_node='\\TS_EDGE'+tmp_idx+':EDGE'+tmp_idx+'_TE'
           Ne_node='\\TS_EDGE'+tmp_idx+':EDGE'+tmp_idx+'_NE'
           R_node='\\TS_EDGE'+tmp_idx+':EDGE'+tmp_idx+'_POS'
           TSTePARAMETERS.append(Te_node);
           TSNePARAMETERS.append(Ne_node);
           TSRADIUS.append(R_node);



    tste=[];
    tsne=[];
    tsR=[];
    tstime=[];

    # get all data for PARAMETERS
    ts_plot_on=1;
    with MDS(server="172.17.100.200:8005") as mds:
       try:
           eq=mds.open(shot=shot, tree='kstar');
       except:
           print "Error #1"
       else:
           try:
               print mds.alist
               for signame in TSTePARAMETERS:
                   print 'reading ...',signame
                   temp = eq.get(signame).data();
                   temp_time=eq.get('dim_of(%s)' %(signame)).data();
                   tstime=temp_time;
                   tste.append(temp)
               for signame in TSNePARAMETERS:
                   print 'reading ...',signame
                   temp = eq.get(signame).data();
                   tsne.append(temp)
               for signame in TSRADIUS:
                   print 'reading ...',signame
                   temp = eq.get(signame).data();
                   tsR.append(temp);
           except:
               print "Cannot reading the signal\n Quit the program";
               #sys.exit(0);
               ts_plot_on=0;
           else:
               print "END of reading"
    mds.close();

    ptime=input("Insert reference  plot time [sec] : ");
    if (ces_plot_on ==1):
       tmp_time=[]; #CES
       tmp_time=cestime-ptime;
       tmp_time=np.abs(tmp_time);
       ptime_idx=np.where(tmp_time==min(tmp_time))[0];
    if (ts_plot_on == 1):
       tmp_time=[]; #TS
       tmp_time=tstime-ptime;
       tmp_time=np.abs(tmp_time);
       tsptime_idx=np.where(tmp_time==min(tmp_time))[0];
    
    ptime2=input("Insert plot time [sec] : ");
    if (ces_plot_on == 1):
       tmp_time=[]; #CES
       tmp_time=cestime-ptime2;
       tmp_time=np.abs(tmp_time);
       ptime2_idx=np.where(tmp_time==min(tmp_time))[0];
    if (ts_plot_on == 1):
       tmp_time=[]; #TS
       tmp_time=tstime-ptime2;
       tmp_time=np.abs(tmp_time);
       tsptime2_idx=np.where(tmp_time==min(tmp_time))[0];
     
    
    if (ces_plot_on == 1):    
       majorR=[];
       plotT=[];
       plotV=[];
       plotT2=[];
       plotV2=[];
       cesR2015=[1801., 1822., 1843., 1874., 1895., 1945., 1995., 2016., 2047., 2078., 2099., 2125., 2150., 2171., 2192., 2203., 2213., 2223., 2228., 2233., 2238., 2243., 2248., 2253., 2259., 2264., 2269., 2273., 2280., 2286., 2291., 2296.];
       cesR2014=[1795., 1850., 1900., 1950., 2000., 2050., 2100., 2150., 2170., 2180., 2190., 2200., 2205., 2210., 2215., 2220., 2225., 2230., 2235., 2240., 2245., 2250., 2255., 2260., 2265., 2270., 2275., 2280., 2285., 2290., 2295., 2300.];
       cesR2013=[1795., 1850., 1900., 1950., 2000., 2050., 2100., 2150., 2170., 2180., 2190., 2200., 2205., 2210., 2215., 2220., 2225., 2230., 2235., 2240., 2245., 2250., 2255., 2260., 2265., 2270., 2275., 2280., 2285., 2290., 2295., 2300.];
       cesR2012=[1800., 1850., 1900., 1950., 2000., 2050., 2100., 2150., 2170., 2180., 2190., 2200., 2205., 2210., 2215., 2220., 2225., 2230., 2235., 2240., 2245., 2250., 2255., 2260., 2265., 2270., 2275., 2280., 2285., 2290., 2295., 2300.];
       cesR2011=[1795., 1800., 1850., 1900., 1950., 2000., 2050., 2100., 2140., 2160., 2170., 2180., 2190., 2200., 2205., 2210., 2215., 2220., 2225., 2230., 2235., 2240., 2245., 2250., 2255., 2265., 2275., 2280., 2285., 2290., 2295., 2300.];
       for i in range(1,33):
           if (np.shape(tcesR)[0] < 1 ):
              if (shot < 11727 and shot > 9427):
                 majorR.append(cesR2014[i-1]);
              elif (shot < 9428 and shot > 8355):
                 majorR.append(cesR2013[i-1]);
              elif (shot < 8356 and shot > 6470):
                 majorR.append(cesR2012[i-1]);
              elif (shot < 6471 and shot > 4468):
                 majorR.append(cesR2011[i-1]);
              elif (shot > 11726):
                 majorR.append(cesR2015[i-1]);
           else:    
              majorR.append(tcesR[i-1][ptime_idx[0]]);
           plotT.append(cesti[i-1][ptime_idx[0]]);
           plotV.append(cesvt[i-1][ptime_idx[0]]);
           plotT2.append(cesti[i-1][ptime2_idx[0]]);
           plotV2.append(cesvt[i-1][ptime2_idx[0]]);
       #write file
       plot_time=[cestime[ptime_idx[0]],cestime[ptime2_idx[0]]];
       ces_filename_R='%d_CES_R_%dms_%dms.txt'%(shot,plot_time[0]*1000,plot_time[1]*1000);
       f=open(ces_filename_R,"w");
       f.write('%8s%12s%12s%12s%12s%12s%12s\n'%("R(mm)","Time1(s)","Ti1(eV)","Vt1(km/s)","Time2(s)","Ti2(eV)","Vt2(km/s)"));
       for j in range(0,len(plotT)-1):
           f.write(str("%8d"%majorR[j])+str("%12.3f"%plot_time[0])+str("%12.1f"%plotT[j])+str("%12.1f"%plotV[j])+str("%12.1f"%plot_time[1])+str("%12.1f"%plotT2[j])+str("%12.1f"%plotV2[j])+"\n");
       f.close();

    
    if (ts_plot_on == 1):
       TSmajorR=[];
       plotTe=[];
       plotNe=[];
       plotTe2=[];
       plotNe2=[];
       for i in range(1,28):
           TSmajorR.append(tsR[i-1]);
           plotTe.append(tste[i-1][tsptime_idx[0]]);
           plotNe.append(tsne[i-1][tsptime_idx[0]]);
           plotTe2.append(tste[i-1][tsptime2_idx[0]]);
           plotNe2.append(tsne[i-1][tsptime2_idx[0]]);
       #write file 
       plot_time=[tstime[tsptime_idx[0]],tstime[tsptime2_idx[0]]];
       TS_filename_R='%d_Thomson_R_%dms_%dms.txt'%(shot,plot_time[0]*1000,plot_time[1]*1000);
       f=open(TS_filename_R,"w");
       f.write('%8s%12s%12s%18s%12s%12s%18s\n'%("R(mm)","Time1(s)","Te1(eV)","Ne1(1e19m-3)","Time2(s)","Te2(eV)","Ne2(1e19m-3)"));
       for j in range(0,len(plotTe)-1):
           f.write(str("%8d"%TSmajorR[j])+str("%12.3f"%plot_time[0])+str("%12.0f"%plotTe[j])+str("%18.3f"%(plotNe[j]/1e19))+str("%12.1f"%plot_time[1])+str("%12.0f"%plotTe2[j])+str("%18.3f"%(plotNe2[j]/1e19))+"\n");
       f.close();
    
    if (ces_plot_on == 1):    
       plt.figure(1,figsize=(10,5))

       plt.subplot(1,2,1)
       plt.plot(majorR,plotT,'o--', );
       plt.plot(majorR,plotT2,'s-');
       plt.xlabel('Major R [mm]');
       plt.ylabel('T$_i$ [eV]');
       maxylim=max(plotT[1],plotT2[1])
       plt.ylim([0,maxylim*1.2])
       plt.xlim([1800, 2300])
       plt.legend([str(cestime[ptime_idx[0]])+' sec', str(cestime[ptime2_idx[0]])+' sec'])

       plt.subplot(1,2,2)
       plt.plot(majorR,plotV,'o--');
       plt.plot(majorR,plotV2,'s-');
       plt.xlabel('Major R [mm]');
       plt.ylabel('V$_t$ [km/s]');
       maxylim=max(plotV[1],plotV2[1])
       plt.ylim([0,maxylim*1.2])
       plt.xlim([1800, 2300])
       plt.legend([str(cestime[ptime_idx[0]])+' sec', str(cestime[ptime2_idx[0]])+' sec'])
       #plt.show()
       #print cestime
    
    if (ts_plot_on == 1):    
       plt.figure(2,figsize=(10,5))

       plt.subplot(1,2,1)
       plt.plot(tsR,plotTe,'o--');
       plt.plot(tsR,plotTe2,'s-');
       plt.xlabel('Major R [mm]');
       plt.ylabel('T$_e$ [eV]');
       maxylim=max(plotTe[1],plotTe2[1])
       plt.ylim([0,maxylim*1.2])
       plt.xlim([1800, 2300])
       plt.legend([str(tstime[tsptime_idx[0]])+' sec', str(tstime[tsptime2_idx[0]])+' sec'])

       plt.subplot(1,2,2)
       plt.plot(tsR,plotNe,'o--');
       plt.plot(tsR,plotNe2,'s-');
       plt.xlabel('Major R [mm]');
       plt.ylabel('N$_e$ [m$^{-3}$]');
       maxylim=max(plotNe[1],plotNe2[1])
       plt.ylim([0,maxylim*1.2])
       plt.xlim([1800, 2300])
       plt.legend([str(tstime[tsptime_idx[0]])+' sec', str(tstime[tsptime2_idx[0]])+' sec'])
       plt.show()
       
    


    # get rtEFIT data in PARAMETERS
    PARAMETERS=['\\bcentr','\\bdry','\\cpasma','\\epoten','\\ffprim',
                '\\fpol','\\gtime','\\lim','\\limitr','\\mh','\\mw','\\nbdry',
                '\\pprime','\\pres','\\psin','\\psirz','\\qpsi','\\r','\\rgrid1',
                '\\rhovn','\\rmaxis','\\rzero','\\ssibry','\\ssimag','\\xdim','\\z',
                '\\zdim','\\zmaxis','\\zmid'];
   
    with MDS(server="172.17.100.200:8005") as mds:
       try:
           eq=mds.open(shot=shot, tree='efitrt1');
       except:
           print "Error #1"
       else:
           try:
               print mds.alist
               for signame in PARAMETERS:
                   print 'reading ...',signame
                   temp = eq.get(signame).data();
                   geqdsk.append(temp);
           except:
               print "Cannot reading the signal\n Quit the program";
               sys.exit(0);
           else:
               print "END of reading"
    mds.close();


    index_time = PARAMETERS.index('\\gtime');
    
    if( time_i < geqdsk[index_time][0] ): # Check the minimum time slice
        time_i = geqdsk[index_time][0];
        print "The initial time reset to", time_i;
    
    if( time_f > geqdsk[index_time][len(geqdsk[index_time])-1] ): # Check the maximum time slice
        time_f =  geqdsk[index_time][len(geqdsk[index_time])-1]
        print "The final time set to", time_f;
    
    timerange = np.arange(time_i,time_f+0.1*t_interval,t_interval);
    
    #filelist=[];
    
    cesefit_idx=[];
    if (ces_plot_on==1):
       cesptime=[cestime[ptime_idx[0]], cestime[ptime2_idx[0]]];
       efittime=geqdsk[index_time];
       #cesefit_idx=[];
       for maptime in cesptime:
           tmp_time=[];
           tmp_time=efittime-maptime;
           tmp_time=np.abs(tmp_time);
           tmp=np.where(tmp_time==min(tmp_time))[0];
           cesefit_idx.append(tmp[0]);

    
    # extract rho_pol according to tcesR
    rho_pol=[];
    loop_idx=0;
    for i in cesefit_idx:
        loop_idx=loop_idx+1;		
        time = geqdsk[index_time][i];
        
        rmaxis = geqdsk[PARAMETERS.index('\\rmaxis')][i];
    
        simag  = geqdsk[PARAMETERS.index('\\ssimag')][i]; 
        sibry  = geqdsk[PARAMETERS.index('\\ssibry')][i];
    
        
        rg=geqdsk[PARAMETERS.index('\\r')]; 
        zg=geqdsk[PARAMETERS.index('\\z')];
        zg_tmp=np.zeros(33);
        psirz=[]
        psirz.append(geqdsk[PARAMETERS.index('\\psirz')][i])
        cesR=[];
        cesZ=np.zeros(32);
        zidx=np.where(zg==0)[0] # interpolation for z = 0
        #print 'majorR=',  majorR, 'np.shape=', np.shape(majorR)
        for j in range(1,33):
            tmp=majorR[j-1]/1000;
            cesR.append(tmp);
            if (cesR[j-1]<rmaxis):
               if (loop_idx == 1):
		  plotT[j-1]=0
                  plotV[j-1]=0
               else:
                  plotT2[j-1]=0
                  plotV2[j-1]=0
        
        
        ip1=interp1d(rg,psirz[0][:][zidx])
        #print 'cesR=', cesR
        zi=ip1(cesR)
        rho_pol_tmp=np.sqrt((zi-simag)/(sibry-simag)); 
        rho_pol.append(rho_pol_tmp[0]);
    
    if (ces_plot_on==1):
       #write file
       plot_time=[cestime[ptime_idx[0]],cestime[ptime2_idx[0]]];
       ces_filename_rho='%d_CES_rho_%dms_%dms.txt'%(shot,plot_time[0]*1000,plot_time[1]*1000);
       f=open(ces_filename_rho,"w");
       f.write('%8s%12s%15s%12s%12s%12s%15s%12s%12s\n'%("R(mm)","Time1(s)","rho_pol(arb)","Ti1(eV)","Vt1(km/s)","Time2(s)","rho_pol(arb)","Ti2(eV)","Vt2(km/s)"));
       for j in range(0,len(plotT)-1):
           f.write(str("%8d"%majorR[j])+str("%12.3f"%plot_time[0])+str("%15.4f"%rho_pol[0][j])+str("%12.1f"%plotT[j])
                   +str("%12.1f"%plotV[j])+str("%12.1f"%plot_time[1])+str("%15.4f"%rho_pol[1][j])+str("%12.1f"%plotT2[j])+str("%12.1f"%plotV2[j])+"\n");
       f.close();

    tsefit_idx=[];
    if (ts_plot_on==1):    
       tsptime=[tstime[tsptime_idx[0]], tstime[tsptime2_idx[0]]];
       efittime=geqdsk[index_time];
       #tsefit_idx=[];
       for maptime in tsptime:
           tmp_time=[];
           tmp_time=efittime-maptime;
           tmp_time=np.abs(tmp_time);
           tmp=np.where(tmp_time==min(tmp_time))[0];
           tsefit_idx.append(tmp[0]);

       print 'EFIT time for Thomson',efittime[tsefit_idx[0]]
    
    # extract rho_pol according to tcesR
    tsrho_pol=[];
    loop_idx=0;
    for i in tsefit_idx:
        loop_idx=loop_idx+1;		
        time = geqdsk[index_time][i];
        
        rmaxis = geqdsk[PARAMETERS.index('\\rmaxis')][i];
    
        simag  = geqdsk[PARAMETERS.index('\\ssimag')][i]; 
        sibry  = geqdsk[PARAMETERS.index('\\ssibry')][i];
    
        
        rg=geqdsk[PARAMETERS.index('\\r')]; 
        zg=geqdsk[PARAMETERS.index('\\z')];
        zg_tmp=np.zeros(33);
        psirz=[]
        psirz.append(geqdsk[PARAMETERS.index('\\psirz')][i])
        thomsonR=[];
        zidx=np.where(zg==0)[0] # interpolation for z = 0
        for j in range(1,28):
            tmp=TSmajorR[j-1]/1000;
            thomsonR.append(tmp);
            if (thomsonR[j-1]<rmaxis):
               if (loop_idx == 1):
		  plotTe[j-1]=0
                  plotNe[j-1]=0
               else:
                  plotTe2[j-1]=0
                  plotNe2[j-1]=0
        
        ip1=interp1d(rg,psirz[0][:][zidx])
        zi=ip1(thomsonR)
        tsrho_pol_tmp=np.sqrt((zi-simag)/(sibry-simag)); 
        tsrho_pol.append(tsrho_pol_tmp[0]);
        
    if (ts_plot_on==1):            
       #write file
       plot_time=[tstime[tsptime_idx[0]],tstime[tsptime2_idx[0]]];
       TS_filename_rho='%d_Thomson_rho_%dms_%dms.txt'%(shot,plot_time[0]*1000,plot_time[1]*1000);
       f=open(TS_filename_rho,"w");
       f.write('%8s%12s%15s%12s%18s%12s%15s%12s%18s\n'%("R(mm)","Time1(s)","rho_pol(arb)","Te1(eV)","Ne1(1e19m-3)","Time2(s)","rho_pol(arb)","Te2(eV)","Ne2(1e19m-3)"));
       for j in range(0,len(plotTe)-1):
           f.write(str("%8d"%TSmajorR[j])+str("%12.3f"%plot_time[0])+str("%15.4f"%tsrho_pol[0][j])+str("%12.0f"%plotTe[j])
                   +str("%18.3f"%(plotNe[j]/1e19))+str("%12.1f"%plot_time[1])+str("%15.4f"%tsrho_pol[1][j])+str("%12.0f"%plotTe2[j])+str("%18.3f"%(plotNe2[j]/1e19))+"\n");
       f.close();
            
    del geqdsk;
    
    # plot CES data according to rho_pol

    if (ces_plot_on ==1):
       plt.figure(3,figsize=(10,5))
       plt.subplot(1,2,1)
       plt.plot(rho_pol[0],plotT,'o--');
       plt.plot(rho_pol[1],plotT2,'s-');
       plt.xlabel(r'$\rho_{pol}$',fontsize=15);
       plt.ylabel('T$_i$ [eV]');
       maxylim=max(max(plotT),max(plotT2))
       #plt.ylim([0,maxylim*1.2])
       plt.xlim([0, 1])
       plt.legend([str(cestime[ptime_idx[0]])+' sec', str(cestime[ptime2_idx[0]])+' sec'])
    

       plt.subplot(1,2,2)
       plt.plot(rho_pol[0],plotV,'o--');
       plt.plot(rho_pol[1],plotV2,'s-');
       plt.xlabel(r'$\rho_{pol}$',fontsize=15);
       plt.ylabel('V$_t$ [km/s]');
       maxylim=max(max(plotV),max(plotV2))
       #plt.ylim([0,maxylim*1.2])
       plt.xlim([0, 1])
       plt.legend([str(cestime[ptime_idx[0]])+' sec', str(cestime[ptime2_idx[0]])+' sec'])


    # plot TS data according to rho_pol
    if (ts_plot_on ==1):
       plt.figure(4,figsize=(10,5))
       plt.subplot(1,2,1)
       plt.plot(tsrho_pol[0],plotTe,'o--');
       plt.plot(tsrho_pol[1],plotTe2,'s-');
       plt.xlabel(r'$\rho_{pol}$',fontsize=15);
       plt.ylabel('T$_e$ [eV]');
       plt.xlim([0, 1])
       plt.legend([str(tstime[tsptime_idx[0]])+' sec', str(tstime[tsptime2_idx[0]])+' sec'])
    

       plt.subplot(1,2,2)
       plt.plot(tsrho_pol[0],plotNe,'o--');
       plt.plot(tsrho_pol[1],plotNe2,'s-');
       plt.xlabel(r'$\rho_{pol}$',fontsize=15);
       plt.ylabel('N$_e$ [km/s]');
       plt.xlim([0, 1])
       maxylim=max(plotNe[1],plotNe2[1])
       plt.ylim([0,maxylim*1.2])
       plt.legend([str(tstime[tsptime_idx[0]])+' sec', str(tstime[tsptime2_idx[0]])+' sec'])

    plt.show()

    

		             
#--------------------------------------------------------------------------------#
if __name__=='__main__':
   """ """
   import os, sys
   import re
   import numpy as np
   import matplotlib.pyplot as plt
   import ctypes
   from   optparse import OptionParser 
   
   exename=os.path.basename(__file__);
   nargs=len(sys.argv);

   usage = "usage: %prog shotnumber";
   parser = OptionParser(usage=usage);
   parser.add_option("-t","--tree", dest="tree",help="MDSplus efit tree",default="kstar");
   (options, args) = parser.parse_args();

   if(nargs<2):
      parser.print_help()
      sys.exit(0);
   
   shot=int(sys.argv[1]);

   time_i = 0.;
   time_f = 1000.;
   t_interval = 0.1;

   if ((nargs >= 3)): time_i = float(sys.argv[2]);
   if ((nargs >= 4)): time_f = float(sys.argv[3]);
   
   tree=options.tree;

   filelist=run(shot,time_i,time_f,t_interval,treename=tree);


