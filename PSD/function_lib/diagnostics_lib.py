"""
this module will conduct diagnostic analysis for plasmas
chunan@ipp.ac.cn 2018/06/13
"""
import numpy
import pylab
from scipy import signal

pi = numpy.pi
# load user defined modules inside function_lib
from . import plot_lib
from . import signal_lib
from . import math_lib
from . import readdata_lib




def heating_all(sig_names = ['LHW', 'NBI', 'ICRF', 'ECRH'], shot = 78010, 
                t_in = [2, 8], i_plot = 1) :
    """
    Calculate the heating power of all heating methods in EAST: 
    Inputs: sig_name = ['LHW', 'NBI', 'ICRF', 'ECRH'] or other combination
    Outputs: total power in MW
    chunan@ipp.ac.cn 2018.07.07
    """
    # define an empty dictionary to store different powers with non-equal sampling. 
    P_dic = {}
    for i in range(0, len(sig_names)) :
        Pi, ti = heating_power(sig_name = sig_names[i], shot = shot, 
                                 t_in = t_in, i_plot = i_plot)
        P_dic['P_' + sig_names[i]] = 0.001*math_lib.moving_average(sig = Pi, 
                                     n = 200)
        P_dic['t_' + sig_names[i]] = ti
        
    if i_plot == 1 :
        pylab.figure(figsize=[10,8])
        for i in range(0, len(sig_names)) :
            t_i = P_dic['t_' + sig_names[i]]
            P_i = P_dic['P_' + sig_names[i]]
            pylab.plot(t_i, P_i)
            pylab.hold('on')
            
        pylab.legend(sig_names, loc = 'best')
        pylab.xlabel('t(s)')
        pylab.ylabel('power (MW)')
        pylab.xlim(t_in)
        pylab.title('EAST #' + str(shot))
        plot_lib.single_plot_paras()
        
    P_dic['test'] = 0
    return P_dic
        



def heating_power(sig_name = 'LHW', shot = 78010, t_in = [2, 8], i_plot = 1) :
    """
    Calculate heating power of EAST for: LHW, ECRH, NBI and ICRF
    signame = 'LHW', 'ECRH', 'NBI' or 'ICRF'
    chunan@ipp.ac.cn 2018.07.07
    """
    if sig_name == 'LHW':
        # P1: 2.45 GHz LHW injection and reflection power in kW
        P1_in, t , unit= readdata_lib.read_signal_fast(shot = shot, sig_name = 'PLHI1', 
        t_in = t_in)
        P1_out, _, _ = readdata_lib.read_signal_fast(shot = shot, sig_name = 'PLHR1', 
        t_in = t_in)
        # P2: 4.6 GHz LHW injection and reflection power in kW
        P2_in, t, _ = readdata_lib.read_signal_fast(shot = shot, sig_name = 'PLHI2', 
        t_in = t_in)
        P2_out, _, _ = readdata_lib.read_signal_fast(shot = shot, sig_name = 'PLHR2', 
        t_in = t_in)
        P1_all = P1_in - P1_out
        P2_all = P2_in - P2_out
        P_all = P1_all + P2_all
        if i_plot == 1 :
            pylab.figure(figsize = (8, 6))
            pylab.plot(t, P1_all, '-', t, P2_all, '-', t, P_all, '--')
            pylab.legend(['LHW2.45GHz', 'LHW4.6GHz', 'LHW all'], loc = 'best')
            pylab.xlabel('t(s)')
            pylab.ylabel('power (kW)')
            pylab.xlim(t_in)
            pylab.title('EAST #' + str(shot))
            plot_lib.single_plot_paras()

    if sig_name == 'LHW245' :
        # P1: 2.45 GHz LHW injection and reflection power in kW
        P1_in, t , unit = readdata_lib.read_signal_fast(shot = shot, 
                         sig_name = 'PLHI1', t_in = t_in)
        P1_out, _, _ = readdata_lib.read_signal_fast(shot = shot, 
                       sig_name = 'PLHR1', t_in = t_in)
        P_all = P1_in - P1_out

    if sig_name == 'LHW46' :
        # P1: 2.45 GHz LHW injection and reflection power in kW
        P2_in, t , unit= readdata_lib.read_signal_fast(shot = shot, 
                         sig_name = 'PLHI2', t_in = t_in)
        P2_out, _, _ = readdata_lib.read_signal_fast(shot = shot, 
                       sig_name = 'PLHR2', t_in = t_in)
        P_all = P2_in - P2_out
        
    if sig_name == 'ICRF' :
        # calculate the heating power of ICRF
        P_in_names = ['PICRF1I', 'PICRF2I', 'PICRF3I', 'PICRF4I', 'PICRF5I', 
        'PICRF6I', 'PICRF7I', 'PICRF8I']
        P_out_names = ['PICRF1R', 'PICRF2R', 'PICRF3R', 'PICRF4R', 'PICRF5R',
        'PICRF6R', 'PICRF7R', 'PICRF8R']
        P_in_matrix, t = readdata_lib.read_signal_matrix(tree = 'analysis', 
        shot = shot, sig_names = P_in_names, t_in = t_in)
        P_out_matrix, _ = readdata_lib.read_signal_matrix(tree = 'analysis', 
        shot = shot, sig_names = P_out_names, t_in = t_in)
        P_in = numpy.sum(P_in_matrix, axis = 1)
        P_out = numpy.sum(P_out_matrix, axis = 1)
        P_all = P_in - P_out
        if i_plot == 1 :
            pylab.figure(figsize = (8, 6))
            pylab.plot(t, P_in, '-', t, P_out, '-', t, P_all, '--')
            pylab.legend(['ICRF in', 'ICRF out', 'ICRF all'], loc = 'best')
            pylab.xlabel('t(s)')
            pylab.ylabel('power (kW)')
            pylab.xlim(t_in)
            pylab.title('EAST #' + str(shot))
            plot_lib.single_plot_paras()
            
    if sig_name == 'ECRH' :
        # calculate the heating power of ECRH
        P_in_names = ['PECRH1I', 'PECRH2I', 'PECRH3I', 'PECRH4I']
        P_in_matrix, t = readdata_lib.read_signal_matrix(tree = 'analysis', 
        shot = shot, sig_names = P_in_names, t_in = t_in)
        P_in = numpy.sum(P_in_matrix, axis = 1)
        P_all = P_in
        if i_plot == 1 :
            pylab.figure(figsize= (8, 6))
            pylab.plot(t, P_in, '-')
            pylab.legend(['ECRH in',], loc = 'best')
            pylab.xlabel('t(s)')
            pylab.ylabel('power (kW)')
            pylab.xlim(t_in)
            pylab.title('EAST #' + str(shot))
            plot_lib.single_plot_paras()

    if sig_name == 'ECRH1' :
        # calculate the heating power of ECRH1
        P_in_names = ['PECRH1I']
        P_in_matrix, t = readdata_lib.read_signal_matrix(tree = 'analysis', 
        shot = shot, sig_names = P_in_names, t_in = t_in)
        P_in = numpy.sum(P_in_matrix, axis = 1)
        P_all = P_in

    if sig_name == 'NBI' :
        # calcualte the heating power of NBI
        U_names = ['NBI1LHV', 'NBI1RHV', 'NBI2LHV', 'NBI2RHV']
        I_names = ['NBI1LHI', 'NBI1RHI', 'NBI2LHI', 'NBI2RHI']
        P1_names = ['PNBI1LSOURCE', 'PNBI1RSOURCE']
        P2_names = ['PNBI2LSOURCE', 'PNBI2RSOURCE']
        i_method = 1
        if i_method == 1 :        
            # heating power is estimated with: P_NBI = U*I*0.5
            # voltage of NBI source, unit = V
            U_matrix, t = readdata_lib.read_signal_matrix(tree = 'east', 
            shot = shot, sig_names = U_names, t_in = t_in)
            # current of NBI source, unit = A
            I_matrix, _ = readdata_lib.read_signal_matrix(tree = 'east', 
            shot = shot, sig_names = I_names, t_in = t_in)
            P_UI = U_matrix*I_matrix*0.5/1000
            P1 = numpy.sum(P_UI[:, 0:2], axis = 1)
            P2 = numpy.sum(P_UI[:, 2:4], axis = 1)    
        elif i_method == 2 :
            # This power is not correct. It is the direction multiply of U*I
            # Which means the default absorb rate is set as 1 with:
            # P_NBI = U*I
            # power of NBI source 1, unit = kW
            P1_matrix, t = readdata_lib.read_signal_matrix(tree = 'analysis', 
            shot = shot, sig_names = P1_names, t_in = t_in)
            # power of NBI source 2, unit = kW
            P2_matrix, _ = readdata_lib.read_signal_matrix(tree = 'analysis', 
            shot = shot, sig_names = P2_names, t_in = t_in)
            P1 = numpy.sum(P1_matrix, axis = 1)
            P2 = numpy.sum(P2_matrix, axis = 1)        
        P_all = P1 + P2
        if i_plot == 1 :
            pylab.figure(figsize = (8, 6))
            pylab.plot(t, P1, '-', t, P2, '-', t, P_all, '--')
            pylab.legend(['NBI 1','NBI 2', 'NBI all'])
            pylab.xlabel('t(s)')
            pylab.ylabel('power (kW)')
            pylab.xlim(t_in)
            pylab.title('EAST #' + str(shot))
            plot_lib.single_plot_paras()

    if sig_name == 'NBI1' :
        # calcualte the heating power of NBI
        U_names = ['NBI1LHV', 'NBI1RHV']
        I_names = ['NBI1LHI', 'NBI1RHI']
        i_method = 1
        if i_method == 1 :        
            # heating power is estimated with: P_NBI = U*I*0.5
            # voltage of NBI source, unit = V
            U_matrix, t = readdata_lib.read_signal_matrix(tree = 'east', 
            shot = shot, sig_names = U_names, t_in = t_in)
            # current of NBI source, unit = A
            I_matrix, _ = readdata_lib.read_signal_matrix(tree = 'east', 
            shot = shot, sig_names = I_names, t_in = t_in)
            P_UI = U_matrix*I_matrix*0.5/1000
            P1 = numpy.sum(P_UI, axis = 1)
        P_all = P1

    if sig_name == 'NBI2' :
        # calcualte the heating power of NBI
        U_names = ['NBI2LHV', 'NBI2RHV']
        I_names = ['NBI2LHI', 'NBI2RHI']
        i_method = 1
        if i_method == 1 :        
            # heating power is estimated with: P_NBI = U*I*0.5
            # voltage of NBI source, unit = V
            U_matrix, t = readdata_lib.read_signal_matrix(tree = 'east', 
            shot = shot, sig_names = U_names, t_in = t_in)
            # current of NBI source, unit = A
            I_matrix, _ = readdata_lib.read_signal_matrix(tree = 'east', 
            shot = shot, sig_names = I_names, t_in = t_in)
            P_UI = U_matrix*I_matrix*0.5/1000
            P2 = numpy.sum(P_UI, axis = 1)
        P_all = P2

    return P_all, t




def contour_check(sig_matrix = 0, angle = 0, t = 0, f_range = [0, 0], i_test = 0
    , nfft = 1024*4) :
    """check the contour plot of a MHD mode"""
    if i_test == 1 :
        sig_matrix, t = signal_lib.test_data(dim = 2, f_MHD = 10*1000)
        f_range = [9*1000, 11*1000]
    nsig = sig_matrix.shape[1]
    angle = numpy.linspace(0, 2*pi*(nsig-1.0)/nsig, nsig)
    # perform frequency filter to real signal
    sig1_fit, t_fit = signal_lib.FIR_filter(sig = sig_matrix[:, 0], t = t, 
    f_low = f_range[0], f_high = f_range[1], i_plot = 1, n = nfft)
    # generate data matrix to store the filtered signals
    sig_fit_matrix= numpy.zeros([sig1_fit.shape[0], nsig])
    for i in range(0, nsig) :
        sig_fit_matrix[:, i], _ = signal_lib.FIR_filter(sig_matrix[:, i], 
        t = t, f_low = f_range[0], f_high = f_range[1], n = nfft)
    pylab.figure(figsize = (10, 8))    
    pylab.contourf(t_fit, angle*180/pi, sig_fit_matrix.T, 50, cmap = 'jet')
    pylab.colorbar(format='%.2f')
    pylab.title('Filtered in [' + str(numpy.round(f_range[0]/1000, 1)) 
                + ', ' + str(numpy.round(f_range[1]/1000, 1)) + '] kHz')
    pylab.xlabel('t(s)')
    pylab.ylabel('angle(degree)')
    f_MHD = numpy.mean(f_range)
    dt = 1.0/f_MHD
    t_check = numpy.mean(t_fit)
    pylab.xlim([t_check, t_check + 10*dt])
    plot_lib.single_plot_paras()
    pylab.grid('off')
    



def reverse_check(sig_matrix1 = 0, sig_matrix2 = 0, f_range = [0, 0], 
    nfft = 1024, sig_names1 = 0, sig_names2 = 0, shot_name ='TEST_000', 
    i_test = 0, nx = 5, t = 0, t_check = 0) :
    """
    check the reverse of signal on oppostie probes with filtered signals
    chunan@ipp.ac.cn 2018.06.22
    """
    if i_test == 1 :
        print 'i_test == 1'
        sig_matrix1, t = signal_lib.test_data(dim = 2, f_MHD = 5*1000)                
        # sig_matrix2 just make an reverse order of the original sig_matrix1
        sig_matrix2, _ = signal_lib.test_data(dim = 2, f_MHD = 5*1000, 
                                              shift = pi)
        sig_matrix2 = sig_matrix2*0.5
        f_range = [4*1000, 6*1000]

    nsig = sig_matrix1.shape[1]
    # prepare fack signal names for test
    if sig_names1 == 0 :
        sig_names1 = ['A_sig0']
        sig_names2 = ['B_sig0']
        for i in range(1, nsig) :
            sig_names1.append('A_sig' + str(i))        
            sig_names2.append('B_sig' + str(i))
            
    # set the time to check the MHD oscillation
    if t_check == 0 :
        t_check = numpy.mean(t)
    
    # perform frequency filter to real signal
    sig1_fit, t_fit = signal_lib.FIR_filter(sig = sig_matrix1[:, 0], t = t, 
    f_low = f_range[0], f_high = f_range[1], i_plot = 1, n = nfft)
    # generate data matrix to store the filtered signals
    sig_fit_matrix1= numpy.zeros([sig1_fit.shape[0], nsig])
    sig_fit_matrix2 = numpy.zeros([sig1_fit.shape[0], nsig])

    for i in range(0, nsig) :
        sig_fit_matrix1[:, i], _ = signal_lib.FIR_filter(sig_matrix1[:, i], 
        t = t, f_low = f_range[0], f_high = f_range[1], n = nfft)
        sig_fit_matrix2[:, i], _ = signal_lib.FIR_filter(sig_matrix2[:, i], 
        t = t, f_low = f_range[0], f_high = f_range[1], n = nfft)
    
    # calculate the number of rows for subplot
    ny = numpy.ceil(nsig*1.0/nx)
    pylab.figure(figsize = (16, 10))    
    for i in range(0, nsig) :
        if i == 0 :
            ax1 = pylab.subplot(ny, nx, i + 1)
            pylab.plot(t_fit, sig_fit_matrix1[:, i], '-', color = 'blue') 
            pylab.hold('on')
            pylab.plot(t_fit, sig_fit_matrix2[:, i], '--', color = 'red')
            #pylab.legend([sig_names1[i], sig_names2[i]])
            pylab.title(shot_name)
            ax1.yaxis.tick_right()
        else :
            ax = pylab.subplot(ny, nx, i + 1, sharex = ax1)
            pylab.plot(t_fit, sig_fit_matrix1[:, i], '-', color = 'blue') 
            pylab.hold('on')
            pylab.plot(t_fit, sig_fit_matrix2[:, i], '--', color = 'red')
            ax.yaxis.tick_right()
            #pylab.legend([sig_names1[i], sig_names2[i]])
            if i == 1 :
                pylab.title('Filtered in [' + str(numpy.round(f_range[0]/1000, 1)) 
                + ', ' + str(numpy.round(f_range[1]/1000, 1)) + '] kHz')
            #pylab.legend([sig_names1[i], sig_names2[i]])        
        f_MHD = numpy.mean(f_range)
        dt = 1.0/f_MHD
        pylab.xlim([t_check, t_check + 8*dt])
        pylab.xlabel('t(s)')
        pylab.ylabel(sig_names1[i] + '&' + sig_names2[i])        
        # pylab.ylabel('Amp')
        plot_lib.single_plot_paras(fontsize = 12)
    pylab.tight_layout()
    #pylab.show()        




def array_psd(sig_matrix = 0, t = 0, sig_names = 0, nx = 5, i_plot = 1, 
              i_test = 0, nfft = 1024*10, shot_name = 'TEST #0') :
    """
    dispaly the PSD and orignal signal for an array of signals
    chunan@ipp.ac.cn 2018.06.21
    """
    if i_test == 1 :
        sig_matrix, t = signal_lib.test_data(dim = 2)
        # column of figures to display in x direction
    # get the number of signals
    nsig = sig_matrix.shape[1]
    if sig_names == 0 :
        sig_names = ['sig0']
        for i in range(1, nsig) :
            sig_names.append('sig' + str(i))
    # raw of figures to display in y direction
    ny = numpy.ceil(nsig*1.0/nx)
    dt = (t[2] - t[0])/2.0
    Fs = 1.0/dt
    noverlap = numpy.round(nfft*0.50)
    wind = numpy.hanning(nfft)
    pylab.figure(figsize = (16, 10))
    for i in range(0, nsig) :
        if i == 0 :
            ax1 = pylab.subplot(ny, nx, i + 1)
            f, _, PSD_raw = signal.spectrogram(sig_matrix[:,i], fs = Fs, 
            window = wind, noverlap = noverlap, nperseg = nfft)
            # reconstuct time array
            t_fix = numpy.linspace(t[0], t[len(t)-1], PSD_raw.shape[1])
            # ax1.legend([shot_name,])
            pylab.title(shot_name)
        else :
            pylab.subplot(ny, nx, i + 1, sharex = ax1, sharey = ax1)
            f, _, PSD_raw = signal.spectrogram(sig_matrix[:,i], fs = Fs, window = wind, 
            noverlap = noverlap, nperseg = nfft)               
        PSD_raw_real = numpy.log10(numpy.abs(PSD_raw))
        pylab.contourf(t_fix, f/1000, PSD_raw_real, 100,camp = 'jet')
        pylab.xlim((t_fix[0],t_fix[len(t_fix)-1])) 
        pylab.ylim([0, Fs/2.0/1000])
        pylab.xlabel('t(s)')
        pylab.ylabel('f(kHz) ' + sig_names[i])
        plot_lib.single_plot_paras(fontsize = 12)
        pylab.grid('off')
    pylab.tight_layout()
    pylab.show()




def mode_numbers(sig_matrix1 = 0, sig_matrix2 = 0, t = 0, t_check = 0, 
    coil_angle = 0, f_MHD = 0, df = 1*1000, nfft = 1024, sign = -1, i_test = 0, 
    i_plot = 1, nlim = 3, shot = 00000, xleg = 0) :
    """
    this function will calculate the phase shift between two signal arrays and 
    esticmate the related mode numbers with given coils' shift angle 
    chunan@ipp.ac.cn 2018.06.13
    """
    if i_test == 1 :
        sig_matrix1, t = signal_lib.test_data(dim = 2, shift = 0)                
        # sig_matrix2 just make an reverse order of the original sig_matrix1
        sig_matrix2, _ = signal_lib.test_data(dim = 2, shift = pi/8)

        t_check = numpy.linspace(t[1], t[len(t)-2], 3)
        # theta is the physical angle between two adjecent coils
        coil_angle = 2*pi/16
        f_MHD = 15*1000
        df = 0.1*1000
        nfft = 512*4
        nlim = 3
        shot = 00000
        xleg = 0
        i_plot = 1
        
    # define an empty matrix to store the phase shift data
    ncoil = sig_matrix1.shape[1]
    phase_array = numpy.zeros([ncoil, len(t_check)])
    # generate x axis array
    if xleg == 0 :
        tor_angle = numpy.linspace(0, 2*pi*(ncoil - 1.0)/ncoil, ncoil) 
    else :
        tor_angle = numpy.arange(0, ncoil)
    for i in range(0, len(t_check)) :
        if i == 0:
            phase_array[:, i], f_mode = signal_lib.phase_diff_2matrix(
            sig_matrix1, sig_matrix2, t, t_check[i], f_check = f_MHD, df = df, 
             nfft = nfft, i_plot = i_plot)
        else:
            phase_array[:, i], _ = signal_lib.phase_diff_2matrix(sig_matrix1, 
            sig_matrix2, t, t_check[i], f_check = f_MHD, df = df, nfft = nfft)
    # modify the sign of the phase
    phase_array = phase_array*sign
    if xleg == 0 :    
        tor_angle_dense = numpy.linspace(0, 2*pi, 50)*180/pi
    else :
        tor_angle_dense = numpy.linspace(0, ncoil - 1, 50)
    n_array = numpy.arange(-nlim, nlim + 1)
    # n_array = numpy.array([4, 3, 2, 1, 0, -1 , -2, -3, -4])
    # define y array for the plot of mode n basis lines
    y_array = numpy.zeros([len(tor_angle_dense), len(n_array)])
    for i in range(0, len(n_array)) :
        y_array[:, i] = numpy.ones(len(tor_angle_dense))*coil_angle*n_array[i]
    # generate an empty legend array
    legs = range(len(t_check))
    # lines = ['--', '-.', ':']
    colors = ['red', 'blue', 'green','purple', 'black', 'magenta', 'blue']
    markers = ['o', '<', 's', 'd', 'p', '>', '*', '^']
    # control whether to convert toroidal angle to degree
    if xleg == 0 :
        tor_angle = tor_angle*180/pi
    else :
        tor_angle = tor_angle*1.0
    if i_plot == 1 :
        pylab.figure(figsize = [9, 6])
        ax = pylab.gca()
        # plot phase diff of coils at different time point
        for i in range(0, len(t_check)):
            ax.plot(tor_angle, phase_array[:, i]*180/pi, 
                    markers[math_lib.residue(i, 8)], markersize = 10)
            pylab.hold('on')
            legs[i] = str(numpy.round(t_check[i], 4)) + ' s'
        ax.legend(legs, fontsize = 12, loc = 'upper left')
        # plot the basis lines of different mode n
        for j in range(0, y_array.shape[1]):
            ax.plot(tor_angle_dense, y_array[:, j]*180/pi, '--', 
                    linewidth = 2.5, color = colors[math_lib.residue(j, 7)])
            pylab.hold('on')
            if xleg == 0 :
                pylab.text(365, y_array[0, j]*180/pi, 'n = ' + str(n_array[j]), 
                           color = colors[math_lib.residue(j, 7)], fontsize = 16)
            else :
                # set the relative start postion of font annotation
                x0 = -1 + (ncoil + 1)*17.5/20
                pylab.text(x0, y_array[0, j]*180/pi + 5, 'n = ' + 
                str(n_array[j]), color = colors[math_lib.residue(j, 7)], 
                fontsize = 16)
        pylab.ylim([-coil_angle*(nlim + 0.5)*180/pi, coil_angle*(nlim + 0.5)*180/pi])
        if xleg == 0 :
            pylab.xlim([-10, 410])
            pylab.xlabel('probes (degree)')
        else :
            # set the xtick label as probe names
            pylab.xlim([-1, ncoil])
            ax.set_xticks(tor_angle)
            ax.set_xticklabels(xleg, rotation='vertical', fontsize=12)
        pylab.ylabel('phase shift (degree)')
        pylab.title('#' + str(shot) + ', ' + str(numpy.round(f_mode/1000,1)) 
        + ' kHz, mode number')
        plot_lib.single_plot_paras()
    return phase_array, t_check 




def poloidal_modes(sig_matrix1 = 0, sig_matrix2 = 0, t = 0, t_check = 0, 
    pol_angle = 0, coil_shift = 0, f_MHD = 0, df = 1*1000, nfft = 1024, sign = -1, i_test = 0, 
    i_plot = 1, nlim = 3, shot = 00000, xleg = 0) :
    """
    Calculate phase shift between two signal arrays in poloidal direction 
    and esticmate the related mode numbers with given coils' shift angles
    inputs:
    pol_angle: poloidal angles of Mirnov array, coil shift is calculated from it
    chunan@ipp.ac.cn 2018.06.28
    """
    if i_test == 1 :
        sig_matrix1, t = signal_lib.test_data(dim = 2, shift = 0)                
        # sig_matrix2 just make an reverse order of the original sig_matrix1
        sig_matrix2, _ = signal_lib.test_data(dim = 2, shift = pi/8)
        # sig_matrix2 = sig_matrix1
        t_check = numpy.linspace(t[1], t[len(t)-2], 3)
        # theta is the physical angle between two adjecent coils
        pol_angle = numpy.linspace(-pi, pi*(7.0/8), 16)
        f_MHD = 15*1000
        df = 0.1*1000
        nfft = 512*4
        nlim = 3
        shot = 00000
        xleg = 0
        i_plot = 1

    # define an empty matrix to store the phase shift data
    ncoil = sig_matrix1.shape[1]
    # calculate physical phase shift between adjecant angles
    # coil_shift = math_lib.angle_circle_diff(pol_angle)
    # coil_shift = numpy.abs(coil_shift)
    # coil_shift = math_lib.angle_normal(theta = coil_shift, normal = 1)
    # prepare empty array to store signal phase shift
    phase_array = numpy.zeros([ncoil, len(t_check)])
    # generate x axis array
    if xleg == 0 :
        pol_angle = pol_angle/pi*180
    # else :
        # pol_angle = numpy.linspace(0, ncoil - 1, 50)

    for i in range(0, len(t_check)) :
        if i == 0 :
            phase_array[:, i], f_mode = signal_lib.phase_diff_2matrix(
            sig_matrix1, sig_matrix2, t, t_check[i], f_check = f_MHD, df = df, 
            nfft = nfft, i_plot = i_plot)
        else :
            phase_array[:, i], _ = signal_lib.phase_diff_2matrix(sig_matrix1, 
            sig_matrix2, t, t_check[i], f_check = f_MHD, df = df, nfft = nfft)

    # modify the sign of the phase
    phase_array = phase_array*sign

    n_array = numpy.arange(-nlim, nlim + 1)
    # n_array = numpy.array([4, 3, 2, 1, 0, -1 , -2, -3, -4])
    # define y array for the plot of mode n basis lines
    y_array = numpy.zeros([len(pol_angle), len(n_array)])

    for i in range(0, len(n_array)) :
        y_array[:, i] = coil_shift*n_array[i]
    # generate an empty legend array
    legs = range(len(t_check))
    # lines = ['--', '-.', ':']
    colors = ['red', 'blue', 'green','purple', 'black', 'magenta', 'blue']
    markers = ['o', '<', 's', 'd', 'p', '>', '*', '^']        
    if xleg != 0 :
        pol_angle = numpy.arange(0, ncoil)
    
    if i_plot == 1 :
        pylab.figure(figsize = [12, 8])
        ax = pylab.gca()
        # plot phase diff of coils at different time point
        for i in range(0, len(t_check)) :
            ax.plot(pol_angle, phase_array[:, i]*180/pi, 
                    markers[math_lib.residue(i, 8)], markersize = 10)
            pylab.hold('on')
            legs[i] = str(numpy.round(t_check[i], 4)) + ' s'

        ax.legend(legs, fontsize = 12, loc = 'upper left')
        # plot the basis lines of different mode n
        for j in range(0, y_array.shape[1]):
            ax.plot(pol_angle, y_array[:, j]*180/pi, 'o', linewidth = 2.5, 
            markersize = 18, markeredgecolor = colors[math_lib.residue(j, 7)],
            markerfacecolor = 'none', markeredgewidth = 2)
            pylab.hold('on')
            if xleg == 0 :
                pylab.text(185, y_array[0, j]*180/pi, 'm = ' + str(n_array[j]), 
                           color = colors[math_lib.residue(j, 7)], fontsize = 16)
            else :
                # set the relative start postion of font annotation
                x0 = -1 + (ncoil + 1)*17.5/20
                pylab.text(x0, y_array[0, j]*180/pi + 5, 'm = ' + 
                str(n_array[j]), color = colors[math_lib.residue(j, 7)], 
                fontsize = 16)
        max_shift = numpy.max(numpy.abs(coil_shift))
        pylab.ylim([-max_shift*(nlim + 0.5)*180/pi, max_shift*(nlim + 0.5)*180/pi])
        if xleg == 0 :
            # pylab.xlim([-10, 410])
            pylab.xlim([-190, 230])
            pylab.xlabel('probes (degree)')
        else :
            # set the xtick label as probe names
            # pol_angle = numpy.linspace(0, ncoil - 1, 50)
            pylab.xlim([-1, ncoil])
            ax.set_xticks(pol_angle)
            ax.set_xticklabels(xleg, rotation='vertical', fontsize=12)
            
        pylab.ylabel('phase shift (degree)')
        pylab.title('#' + str(shot) + ', ' + str(numpy.round(f_mode/1000,1)) 
        + ' kHz, mode number')
        plot_lib.single_plot_paras()

    return phase_array, t_check

