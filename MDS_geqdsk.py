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
def run(shot,time_i,time_f,treename='EFITRT1'):
    """ """
    import os, sys
    import time as time_module
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy import interpolate
      
    PARAMETERS=['\\bcentr','\\bdry','\\cpasma','\\epoten','\\ffprim',
                '\\fpol','\\gtime','\\lim','\\limitr','\\mh','\\mw','\\nbdry',
                '\\pprime','\\pres','\\psin','\\psirz','\\qpsi','\\r','\\rgrid1',
                '\\rhovn','\\rmaxis','\\rzero','\\ssibry','\\ssimag','\\xdim','\\z',
                '\\zdim','\\zmaxis','\\zmid'];
    
    geqdsk=[];
    
    # get all data for PARAMETERS
    with MDS(server="172.17.250.100:8005") as mds:
       try:
           eq=mds.open(shot=shot, tree=treename);
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
    
    for i in range(0,len(geqdsk[index_time])):
        time = geqdsk[index_time][i];
        if(( time >= time_i) and ( time <= time_f )):
             
             # output filename for geqdsk
             time_fileout = time*1000;
             file_name='g%06d.%06d'%(shot,time_fileout);
             print "writing... ",file_name;
             
             f=open(file_name,"w");
    
             nw=geqdsk[PARAMETERS.index('\\mw')][i];
             nh=geqdsk[PARAMETERS.index('\\mh')][i];
    
             rleft  = geqdsk[PARAMETERS.index('\\rgrid1')][i]; 
             rdim   = geqdsk[PARAMETERS.index('\\xdim')][i]; 
             rright = rdim+rleft;
             rcentr = geqdsk[PARAMETERS.index('\\rzero')][i]; 
             zdim   = geqdsk[PARAMETERS.index('\\zdim')][i]; 
             zmid   = geqdsk[PARAMETERS.index('\\zmid')][i];
    
             rmaxis = geqdsk[PARAMETERS.index('\\rmaxis')][i];
             zmaxis = geqdsk[PARAMETERS.index('\\zmaxis')][i];
    
             simag  = geqdsk[PARAMETERS.index('\\ssimag')][i]; 
             sibry  = geqdsk[PARAMETERS.index('\\ssibry')][i];
    
             bcentr = geqdsk[PARAMETERS.index('\\bcentr')][i];
             current= geqdsk[PARAMETERS.index('\\cpasma')][i];
             
             # header
             gt=time_module.localtime(time_module.time());
             date='%02d/%02d/%4d'%(gt.tm_mon,gt.tm_mday,gt.tm_year);
             header = " %-12s %10s #%6d %5dms         0"%(treename,date,shot,time_fileout)+str("%4i"%nw)+str("%4i"%nh)+"\n";
             f.write(header);
    
             f.write(str("%16.9e"%rdim)+str("%16.9e"%zdim)+str("%16.9e"%rcentr)+str("%16.9e"%rleft)+str("%16.9e"%zmid)+"\n");
             f.write(str("%16.9e"%rmaxis)+str("%16.9e"%zmaxis)+str("%16.9e"%simag)+str("%16.9e"%sibry)+str("%16.9e"%bcentr)+"\n");
             f.write(str("%16.9e"%current)+str("%16.9e"%simag)+str("%16.9e"%0)+str("%16.9e"%rmaxis)+str("%16.9e"%0)+"\n");
             f.write(str("%16.9e"%zmaxis)+str("%16.9e"%0)+str("%16.9e"%sibry)+str("%16.9e"%0)+str("%16.9e"%0)+"\n");
    
             # profile 
             write_profile(f,geqdsk[PARAMETERS.index('\\fpol')][i]);
             write_profile(f,geqdsk[PARAMETERS.index('\\pres')][i]);
             write_profile(f,geqdsk[PARAMETERS.index('\\ffprim')][i]);
             write_profile(f,geqdsk[PARAMETERS.index('\\pprime')][i]);
    
             #2D psi ...
             l=0;
             for w in range(nw):
                for h in range(nh):
                   f.write(str("%16.9e"%geqdsk[PARAMETERS.index('\\psirz')][i][w][h]));
                   l=l+1;
                   if(l==5):
                      f.write(str("\n"));
                      l=0;
                  
             if(l>0): f.write(str("\n"))
    
             # qprofile
             write_profile(f,geqdsk[PARAMETERS.index('\\qpsi')][i]);
    
             # bdry
             nbdry = geqdsk[PARAMETERS.index('\\nbdry')][i];
             nlimt = geqdsk[PARAMETERS.index('\\limitr')][i];
             
             f.write(str("%4i"%nbdry)+str("%4i"%nlimt)+str("\n"));
    
             l=0         
             for w in range(nbdry):             
               f.write(str("%16.9e"%geqdsk[PARAMETERS.index('\\bdry')][i][w][0]));
               l=l+1;
               if(l==5):
                      f.write(str("\n"));
                      l=0;
               f.write(str("%16.9e"%geqdsk[PARAMETERS.index('\\bdry')][i][w][1]));
               l=l+1;
               if(l==5):
                      f.write(str("\n"));
                      l=0;
             if(l>0): f.write(str("\n"))
    
             l=0;
             for w in range(nlimt):
               f.write(str("%16.9e"%geqdsk[PARAMETERS.index('\\lim')][w][0]));
               l=l+1;
               if(l==5):
                      f.write(str("\n"));
                      l=0;
               f.write(str("%16.9e"%geqdsk[PARAMETERS.index('\\lim')][w][1]));
               l=l+1;
               if(l==5):
                      f.write(str("\n"));
                      l=0;
             if(l>0): f.write(str("\n"));
             
             # kvtor, rvtor, nmass
             f.write("%5d%16.9e%5d\n" %(0, 1.70, 0));
             
             # rhovn
             write_profile(f,geqdsk[PARAMETERS.index('\\fpol')][i]*0.0);
             
             # keecur
             f.write("%5d\n"%(0));
             
             # namelist 'out1'
             f.write("$out1\n$end\n");
             
             # namelist 'basis'
             f.write("$basis\n$end\n");
             
             # namelist 'chiout'
             f.write("$chiout\n$end\n");
             
             # Final header and fittype
             f.write(" %42s %3s\n"%("","mag"));
             
             f.close();
             
#--------------------------------------------------------------------------------#
if __name__=='__main__':
   """ """
   import os, sys
   import numpy as np
   import matplotlib.pyplot as plt
   
   exename=os.path.basename(__file__);
   nargs=len(sys.argv);
   
   if(nargs<2):
      print "[Usages] %s shot t_start t_end [tree=efitrt]" %(exename);
      sys.exit()
   
   shot=int(sys.argv[1]);

   time_i = 0.;
   time_f = 1000.;
   tree   = 'efitrt1';

   if ((nargs >= 3)): time_i = float(sys.argv[2]);
   if ((nargs >= 4)): time_f = float(sys.argv[3]);
   if ((nargs >= 5)): 
      l,v=(sys.argv[4]).split('=');
      tree=v;
   
   run(shot,time_i,time_f,treename=tree);

