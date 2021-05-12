"""
signal_lib.py module contains routines to do:
* MHD mode number analysis
* time frequency analysis
* frequency filter
2016/10/03 chunan@ipp.ac.cn
"""

import numpy
import scipy
import pylab
from scipy import signal
# import os
# import sys
# from scipy import signal

# load user define modules
from . import readdata_lib
from . import math_lib
from . import plot_lib
# define public parameters
pi = numpy.pi




# ------------------------------------------------------------------------------
# calculate the phase difference of probe array
# inputs: t_check is only a single point
def phase_diff_2matrix(sig_matrix1, sig_matrix2, t, t_check, f_check = 0, 
                       df = 1*1000, nfft = 1024, i_test = 0, i_plot = 0):
    if i_test == 1:
        print 'Test data is loaded.'
        sig_matrix1, t = test_data(dim = 2)
        nsig = sig_matrix1.shape[1]
        # sig_matrix2 just make an reverse order of the original sig_matrix1
        sig_matrix2 = numpy.zeros(sig_matrix1.shape)
        sig_matrix2[:, 0:nsig - 2] = sig_matrix1[:, 1:nsig - 1]
        sig_matrix2[:, nsig - 1] = sig_matrix1[:, 0]
        t_check = (t[0] + (t[len(t) - 1]))/2.0
        i_plot = 1
        
    # i_window = math_lib.find_time_points(t, t_check)  
    # dt = (t[2] - t[0])/2.0
    # Fs = 1.0/dt
    phase_array = numpy.zeros(sig_matrix1.shape[1])
    for i in range(0, sig_matrix1.shape[1]):
        if i == 0 :
            if i_plot == 1 :
                phase_array[i], f_check = phase_diff(sig_matrix1[:, i], sig_matrix2[:, i], t = t, t_check = t_check, f_check = f_check, nfft = nfft, i_plot = i_plot)
            else :
                phase_array[i], f_check = phase_diff(sig_matrix1[:, i],  sig_matrix2[:, i], t = t, t_check = t_check, f_check = f_check, nfft = nfft)

        else :
            phase_array[i], _ = phase_diff(sig_matrix1[:, i], sig_matrix2[:, i], t = t, t_check = t_check, f_check = f_check, df = df, nfft = nfft)

    phase_array_new = phase_array.T

    return phase_array_new, f_check




# ------------------------------------------------------------------------------
# calculate the phase difference of probe array
def phase_diff_array(sig_matrix, t, t_check, f_check = 0, df = 1*1000, nfft = 1024, i_test = 0, i_plot = 0):
    if i_test == 1:
        sig_matrix, t = test_data(dim = 2)
        t_check = (t[0] + (t[len(t) - 1]))/2
        i_plot = 1
    
    # i_window = math_lib.find_time_points(t, t_check)  
    # dt = (t[2] - t[0])/2.0
    # Fs = 1.0/dt
    phase_array = numpy.zeros(sig_matrix.shape[1])
    for i in range(0, sig_matrix.shape[1]+1):
        if i < sig_matrix.shape[1] - 1:
            phase_array[i], _ = phase_diff(sig_matrix[:, i], sig_matrix[:, i + 1], t = t, t_check = t_check, f_check = f_check, df = df, nfft = nfft)
        elif i == sig_matrix.shape[1] - 1:
        # this judgement calculate phase diff between head and tail signals
            if i_plot == 1:
                phase_array[i], f_check = phase_diff(sig_matrix[:, i], sig_matrix[:, 0], t = t, t_check = t_check, f_check = f_check, nfft = nfft, i_plot = i_plot)
            else :
                phase_array[i], f_check = phase_diff(sig_matrix[:, i], sig_matrix[:, 0], t = t, t_check = t_check, f_check = f_check, nfft = nfft)
    
    phase_array_new = phase_array.T
    return phase_array_new, f_check




# ------------------------------------------------------------------------------
# calculate probe signals phase difference and estimate the toroidal and poloidal MHD mode number
# outputs: phi_check in radial angle unit, which is the phase diff of two modes
def phase_diff(sig1, sig2, t, t_check, f_check = 0, df = 1*1000, nfft = 1024, i_test = 0, i_plot = 0):
    if i_test == 1:
        # generate test signals
        sig2D, t = test_data(dim = 2)
        sig1 = sig2D[:, 0]
        sig2 = sig2D[:, 1]
        t_check = (t[0] + (t[len(t) - 1]))/2
        i_plot = 1
        print len(t)
        print t_check
    
    i_window = math_lib.find_time_points(t, t_check)  
    dt = (t[2] - t[0])/2.0
    Fs = 1.0/dt
    window1 = window_a_point(i_window, sig1, nfft)
    window2 = window_a_point(i_window, sig2, nfft)
    A1 = numpy.fft.fft(window1, axis = 0)
    A2 = numpy.fft.fft(window2, axis = 0)
    cpsd = numpy.conj(A1)*A2
    CPSD = cpsd[0:numpy.round(nfft/2)+1]
    A = numpy.abs(CPSD)
    phi = numpy.angle(CPSD)
    f = numpy.linspace(0, Fs/2, len(A))
    # get the index of frequency for check, based on input
    if f_check == 0:
        i_peak = numpy.argmax(A)
    elif f_check > 0:
        index1 = math_lib.find_time_points(f, f_check - df)
        index2 = math_lib.find_time_points(f, f_check + df)
        i_peak = numpy.argmax(A[index1:index2])
        # i_peak = math_lib.find_time_index(f, f_check)        
        i_peak = i_peak + index1

    phi_check = phi[i_peak]
    # phi_check = numpy.mean(phi[i_peak - 1: i_peak + 1])
    f_check = f[i_peak]
    #A_check = A[i_peak]
    if i_plot == 1 :
        pylab.figure()
        pylab.plot(f/1000, A, '-', color = 'blue')
        pylab.hold('on')
        pylab.xlim([f.min()/1000, f.max()/1000])
        pylab.plot(f_check/1000, A[i_peak], 'o', color = 'red')
        pylab.xlabel('f(kHz)')
        pylab.ylabel('Amp')
        pylab.title('signal spectrum near '+str(t_check)+' s')
        plot_lib.single_plot_paras()
        # pylab.show()
    
    return phi_check, f_check 




# ------------------------------------------------------------------------------
# function to do bandpass FIR filter
# subfunctions for filter, Plot frequency and phase response
# refer from: http://mpastell.com/2010/01/18/fir-with-scipy/ 
def mfreqz(b,a=1):
    w,h = signal.freqz(b,a)
    h_dB = 20*numpy.log10(abs(h))

    pylab.figure()    
    pylab.subplot(211)
    pylab.plot(w/max(w),h_dB)
    pylab.ylim(-150, 5)
    pylab.ylabel('Magnitude (db)')
    pylab.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    pylab.title(r'Frequency response')
    
    pylab.subplot(212)
    h_Phase = numpy.unwrap(numpy.arctan2(numpy.imag(h),numpy.real(h)))
    pylab.plot(w/max(w),h_Phase)
    pylab.ylabel('Phase (radians)')
    pylab.xlabel(r'Normalized Frequency (x$\pi$rad/sample)')
    pylab.title(r'Phase response')
    pylab.subplots_adjust(hspace=0.5)
    
    


# ------------------------------------------------------------------------------
# main function of FIR filter
# subfunction for filter, plot phase and impluse response
# refer from: http://mpastell.com/2010/01/18/fir-with-scipy/
def impz(b,a=1):
    l = len(b)
    impulse = numpy.repeat(0.,l)
    impulse[0] =1.
    x = numpy.arange(0,l)
    response = signal.lfilter(b,a,impulse)

    pylab.figure()    
    pylab.subplot(211)
    pylab.stem(x, response)
    pylab.ylabel('Amplitude')
    pylab.xlabel(r'n (samples)')
    pylab.title(r'Impulse response')

    pylab.subplot(212)
    step = numpy.cumsum(response)
    pylab.stem(x, step)
    pylab.ylabel('Amplitude')
    pylab.xlabel(r'n (samples)')
    pylab.title(r'Step response')
    pylab.subplots_adjust(hspace=0.5)




# ------------------------------------------------------------------------------
# subfunction for signal frequency filter
# choose filters: 1 -> low pass, 2 -> high pass, 3-> band pass 
# refer from: http://mpastell.com/2010/01/18/fir-with-scipy/
def FIR_filter(sig, t, f_low, f_high, i_filter=3, n=512, i_plot = 0, i_test = 0):
    # load test data in this module using test_data()
    if i_test == 1:
        sig, t = test_data(dim = 1)
        f_low = 20*1000
        f_high = 40*1000
        i_plot = 1

    dt=(t[2]-t[0])/2
    # calculate sampling frequency
    Fs=numpy.round(1/dt)
    if i_filter==1:
        #low pass filter
        # cutoff frequncy input is normalized by nyquist frequency(Fs/2)
        a = signal.firwin(n, cutoff = f_low/(Fs/2.0), window = "hamming")
        filter_array = a
    elif i_filter==2:
        # high pass filter
        a = signal.firwin(n, cutoff = f_high/(Fs/2.0), window = "hanning")
        # Spectral inversion
        a = -a
        a[n/2] = a[n/2] + 1
        filter_array = a
    elif i_filter == 3:
        # band pass filter
        # design low pass filter
        a=signal.firwin(n,cutoff=f_low/(Fs/2),window='blackmanharris')
        # design Highpass filter
        b = -signal.firwin(n, cutoff =f_high/(Fs/2), window = 'blackmanharris')
        b[n/2] = b[n/2] + 1
        # Combine high pass and low pass filter into a bandpass filter
        d = - (a+b)
        d[n/2] = d[n/2] + 1
        filter_array=d
    # apply filter to signal
    #sig_fit=signal.lfilter(filter_array, 1, sig)
    # both the two codes works for filter the signals
    sig_fit = signal.filtfilt(filter_array,1,sig)
    # plot raw and filter signal and signal PSD to check filter
    i_check = 0
    if i_plot == 1:
        # plot Frequency and phase response        
        mfreqz(filter_array)

        # plot Impulse and step response
        impz(filter_array)
        
        if i_check == 1 :
            # plot raw signal
            pylab.figure()
            pylab.subplot(2,1,1)
            pylab.plot(t,sig)
            pylab.ylabel('raw sig')
            pylab.subplot(2,1,2)
            pylab.plot(t,sig_fit)
            pylab.ylabel('filtered sig')
            # to make a function to realy work, you need add f(), even no inputs 
            pylab.tight_layout()
            # plot PSD of the raw and filtered signal

        pylab.figure()
        ax1 = pylab.subplot(2,1,1)
        # pylab.specgram(sig,NFFT=128,Fs=Fs,noverlap=8)
        NFFT = 128*4
        N_lap = numpy.round(NFFT*0.50)
        wind = signal.hanning(NFFT)
        # wind = signal.gaussian(NFFT, 0.1)
        f, t1, PSD_raw = signal.spectrogram(sig, fs = Fs, window = wind, noverlap = N_lap, nperseg = NFFT)
        # reconstuct time array
        t_fix = numpy.linspace(t[0], t[len(t)-1], PSD_raw.shape[1])
        PSD_raw_real = numpy.log10(numpy.abs(PSD_raw))
        pylab.pcolormesh(t_fix, f/1000, PSD_raw_real)       
        pylab.xlim((t_fix[0],t_fix[len(t_fix)-1])) 
        pylab.ylim([0, Fs/2.0/1000])
        pylab.ylabel('raw PSD (kHz)')

        pylab.subplot(2,1,2, sharex = ax1, sharey = ax1)
        # pylab.specgram(sig_fit,NFFT=128,Fs=Fs,noverlap=8)
        f, t2, PSD_fit = signal.spectrogram(sig_fit, fs = Fs, window = wind, noverlap = N_lap, nperseg = NFFT)
        PSD_fit_real = numpy.log10(numpy.abs(PSD_fit))
        pylab.pcolormesh(t_fix, f/1000, PSD_fit_real)
        pylab.xlim((t_fix[0],t_fix[len(t_fix)-1])) 
        pylab.ylabel('filtered PSD (kHz)')
        pylab.xlabel('t(s)')
        pylab.title('filtered in ['+str(f_low/1000)+','+str(f_high/1000)+'] kHz')
        pylab.tight_layout()
        # pylab.show()
    t_fit = t
    return sig_fit, t_fit
    



# ------------------------------------------------------------------------------
# define function to take data in a small time window
# inputs: i_window should be an ndarray with 2D shape
def window_points(i_window,sig,nfft, i_test=0):
    if i_test == 1:
        sig, t = test_data(dim=1)
        i_window = numpy.array([numpy.round(len(sig)/3.0), numpy.round(len(sig)/3.0*2)])
        print i_window        
        nfft = 512

    # nfft should be a even number
    half_win=numpy.round(nfft/2)
    sig_window_matrix=numpy.zeros((nfft,i_window.shape[0]))
    for i in range (0,i_window.shape[0]):
        if i_window[i]>=half_win and i_window[i]<=sig.shape[0]-half_win :
            sig_window_matrix[:,i]=sig[i_window[i]-half_win:i_window[i]+half_win]
        elif i_window[i]<half_win and i_window[i]>=0:
            sig_window_matrix[:,i]=sig[0:nfft]
        elif i_window[i]>sig.shape[0]-half_win and i_window[i]<sig.shape[0]:
            sig_window_matrix[:,i]=sig[sig.shape[0]-nfft:sig.shape[0]]
        else:
            print 'index out of sig range'
    return sig_window_matrix




# ------------------------------------------------------------------------------
# define function to take data in a small time window
# inputs: i_window should be a pure number
def window_a_point(i_window, sig, nfft, i_test=0):
    if i_test == 1:
        sig, t = test_data(dim=1)
        i_window = numpy.round(len(sig)/3.0)
        print i_window        
        nfft = 512

    # nfft should be a even number
    half_win=numpy.round(nfft/2)
    sig_window=numpy.zeros((nfft))
    if i_window>=half_win and i_window<=sig.shape[0]-half_win :
        sig_window=sig[i_window-half_win:i_window+half_win]
    elif i_window<half_win and i_window>=0:
        sig_window=sig[0:nfft]
    elif i_window>sig.shape[0]-half_win and i_window<sig.shape[0]:
        sig_window=sig[sig.shape[0]-nfft:sig.shape[0]]
    else:
            print 'index i_window out of sig range'
    return sig_window




# ------------------------------------------------------------------------------
# Short Time Fourier Transformamtion to calculate power spectrum density
def psd_STFT(t,sig,points=10,nfft=512,i_plot=0,i_test=0):
    """
    Plot power spectrum for a signal
    Inputs: 
        points # Number of points for faster the speed plot
    """
    if i_test==1:
        pylab.close('all')
        t=numpy.linspace(0,1,10000)
        sig=numpy.sin(2*pi*2400*t)
        omega=2*pi*12000*t
        phi=scipy.integrate.cumtrapz(omega,t,initial=0)
        y=numpy.sin(phi)
        sig=sig+y
        print sig.shape, sig.dtype
        pylab.figure()
        pylab.plot(t,sig)
        pylab.xlabel('t(s)')
        pylab.title('test signal')
        
    # ---- read data from east MDSplus server
    elif i_test==2:
        pylab.close('all')
        sig,t,unit=readdata_lib.read_signal_fast(tree='east',shot=65020,sig_name='KHP7T',t_in=[4,4.2],dn=1,i_plot=1)
        
    # ---- main code for STFT
    dt=(t[2]-t[0])/2
    Fs=1/dt
    i_window=numpy.arange(0, t.shape[0], points)
    #    t_zoom=numpy.linspace(numpy.float(t[0]),numpy.float(t[t.shape[0]-1]),i_window.shape[0])
    t_zoom=numpy.linspace(t[0],t[t.shape[0]-1],i_window.shape[0])
    # generate window function to do smooth
    sig_matrix=window_points(i_window,sig,nfft)
    win=signal.gaussian(nfft,55)
    #win2=signal.hann(nfft,8)
    #win3=signal.hamming(nfft)
    # after compare between gauss, hann and hamming window, I find gauss window
    # with the parameter 55 best fit for smooth with good effect on both
    # x and y direction
    
    # ---- convert the window to fit the shape of signal matrix
    # adjust shape of win function
    win.shape=[win.shape[0],1]
    win_matrix=win*numpy.ones([1,sig_matrix.shape[1]])  
    # apply the window smooth to signal matrix before do fft
    sig_matrix=numpy.multiply(sig_matrix,win_matrix)
    
    # ---- do fft for the windowed signal
    sig_matrix_fft=numpy.fft.fft(sig_matrix,axis=0)/nfft
    # ---- get the real half from fft spectrgram
    #sig_matrix_fft_abs=numpy.multiply(sig_matrix,numpy.conjugate(sig_matrix))
    sig_matrix_fft_abs=numpy.abs(sig_matrix_fft)
    sig_matrix_fft_real=sig_matrix_fft_abs[0:nfft/2+1,:]    
    # prepare time and frequency array
    f=numpy.linspace(0,numpy.float(Fs/2),nfft/2+1)
    t_zoom.shape=[t_zoom.shape[0],1]
    f.shape=[f.shape[0],1]
    
    # ---- plot the spectrum
    if i_plot==1:
        pylab.figure()
        pylab.pcolormesh(t_zoom.T, f/1000, numpy.log(sig_matrix_fft_real),cmap='jet')
        pylab.xlim([t_zoom[0],t_zoom[len(t_zoom)-1]])
        pylab.ylim([0,Fs/2/1000])
        pylab.colorbar()
        pylab.xlabel('t(s)')
        pylab.ylabel('f(kHz)')
        #pylab.show()
        
    # ---- prepare the return value of psd_STFT
    return t_zoom.T, f, sig_matrix_fft_real



def psdplot(sig= 0, t = 0, nfft = 1024, i_test = 0, i_plot = 1) :
    if i_test == 1 :
        sig, t = test_data(dim = 1)
        nfft = 1024*4
        
    dt = (t[2] - t[0])/2.0
    Fs = 1.0/dt    
    noverlap = numpy.round(nfft*0.50)
    wind = numpy.hanning(nfft)
    f, t1, PSD_raw = signal.spectrogram(sig, fs = Fs, window = wind, 
    noverlap = noverlap, nperseg = nfft)
    # reconstuct time array
    t_fix = numpy.linspace(t[0], t[len(t)-1], PSD_raw.shape[1])
    PSD_raw_real = numpy.log10(numpy.abs(PSD_raw))
    if i_plot == 1 :
        pylab.figure(figsize = (10, 8))
        pylab.contourf(t_fix, f/1000, PSD_raw_real, 10)       
        pylab.xlim((t_fix[0],t_fix[len(t_fix)-1])) 
        pylab.ylim([0, Fs/2.0/1000])
        pylab.xlabel('t (s)')
        pylab.ylabel('PSD (kHz)')
        plot_lib.single_plot_paras()
        pylab.grid('off')
        #pylab.show()
        
    return PSD_raw, f, t_fix






# ------------------------------------------------------------------------------
# generate test signal
def test_data(dim = 1, f_MHD = 15*1000, shift = 0, n = 1):
    if dim == 1:
        print 'test data is used: dim = ' + str(dim) + ' f = ' 
        + str(numpy.round(f_MHD/1000,1)) + ' kHz'
        # generate 1 dimensional test signal
        Fs = 100*1000    
        dt = 1.0/Fs
        t = numpy.linspace(1, 1.5, Fs)
        # calculate sampling frequency
        # f1 = 10*1000
        f2 = 25*1000
        f3 = 50*1000        
        y1 = numpy.sin(2*numpy.pi*f_MHD*t)
        y2 = numpy.sin(2*numpy.pi*f2*t)
        y3 = numpy.sin(2*numpy.pi*f3*t)
        sig = y1 + y2 + y3 + 0.1*numpy.random.normal(y1.shape)
    elif dim == 2:
        # generate 2 dimensional test MHD mode measure with sensors
        # str_notice = 'Test mode data loaded! f = ' + 
        # str(numpy.round(f_MHD/1000,1)) + ' kHz' + ' n = ' + str(n) + ' N = 16.'        
        print 'Test mode data loaded! f = ' + str(numpy.round(f_MHD/1000,1)) + ' kHz' + ' n = ' + str(n) + ' N = 16.'
        Fs = 100*1000
        dt = 1.0/Fs
        t = numpy.arange(1, 1.5, dt)
        # suppose the mode has a frequency of 15 kHz
        # f_MHD = 15*1000
        # set the mode n, m of the mode
        # n = 1
        # set the number of probes in toroidal and poloidal direction
        N = 16
        sig = numpy.zeros([len(t), N])
        # set values for signals in toroidal array
        for i in range(0, N):
            sig[:, i] = numpy.cos(2*pi*f_MHD*t + n*2*pi*(i*1.0/N) + shift) 
            + 0.01*numpy.random.normal(sig.shape)

    return sig, t




