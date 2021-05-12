"""
math_lib.py module conduct some basic mathematical calculations which is not
available for default modules like numpy, scipy, etc.
All the functions within this modlue is written by the author: N. Chu 
chunan@ipp.ac.cn 2016/10/03
"""

import numpy
import pylab
# define some commonly seeing parameters
pi = numpy.pi
from . import plot_lib




def moving_average_loop(sig = 0, n = 100, i_test = 0) :
    """
    Perform moving average over n points to smooth signals using loop method
    Loop method on every point will ensure the memorry will not run out
    Here, left average method is adopted.
    """
    if i_test == 1 :
        t = numpy.linspace(0, 1, 1000)
        f = 5
        sig = numpy.sin(2*pi*f*t) + 0.5*numpy.random.normal(t.shape)
    
    sig_ave = numpy.zeros(sig.shape)
    half = numpy.ceil(n/2.0)
    for i in range(0, len(sig)) :
        if i < half:
            # sig_ave[i] = numpy.mean(sig[0:i])
            sig_ave[i] = numpy.mean(sig[i: i + 1*half])
        elif i > len(sig) - half:
            # sig_ave[i] = numpy.mean(sig[i:len(sig) - 1])
            sig_ave[i] = numpy.mean(sig[i - 1*half:i])
        else :
            sig_ave[i] = numpy.mean(sig[i - half:i + half])
    if i_test == 1 :
        print 'sig shape: ', sig.shape
        print 'sig_ave shape: ', sig_ave.shape
        pylab.figure(figsize = (8, 6))
        pylab.plot(t, sig, '->', t, sig_ave, '-<')
        pylab.legend(['raw sig', 'smooth sig'], loc = 'best')
        pylab.xlabel('t(s)')
        plot_lib.single_plot_paras()
    return sig_ave  




def moving_average(sig = 0, n = 5, i_test = 0) :
    """
    Perform moving average over n points to smooth signals
    Here, central average method is adopted.
    """
    if i_test == 1 :
        t = numpy.linspace(0, 1, 100)
        f = 5
        sig = numpy.sin(2*pi*f*t) + 0.5*numpy.random.normal(t.shape)

    sig_ave = numpy.zeros(sig.shape)
    half = numpy.ceil(n/2.0)
    win = numpy.int(2*half)
    sig_ave_matrix = numpy.zeros([len(sig) - win, win])
    i_method = 2
    if i_method == 1 :
        # perform left average method
        for i in range(0, win) :
            sig_ave_matrix[:, i] = sig[i:len(sig) + i - win]
            sig_ave[len(sig) - i - 1] = numpy.mean(sig[len(sig) - win - i:len(sig) -1])
        sig_ave[0:len(sig) - win] = numpy.mean(sig_ave_matrix, axis = 1)
    elif i_method == 2 :
        # perfom central average method
        for i in range(0, win) :
            sig_ave_matrix[:, i] = sig[i:len(sig) + i - win]
            if i < half :
                sig_ave[i] = numpy.mean(sig[0:i + 1])
            elif i >= half :
                sig_ave[len(sig) - (i - half) - 1] = numpy.mean(
                sig[len(sig) - (i - half) - 1:len(sig) - 1])
        sig_ave[half:len(sig) - half] = numpy.mean(sig_ave_matrix, axis = 1)
    if i_test == 1 :
        print 'sig shape: ', sig.shape
        print 'sig_ave shape: ', sig_ave.shape
        pylab.figure(figsize = (8, 6))
        pylab.plot(t, sig, '->', t, sig_ave, '-<')
        pylab.legend(['raw sig', 'smooth sig'], loc = 'best')
        pylab.xlabel('t(s)')
        plot_lib.single_plot_paras()
    return sig_ave        
        



def angle_normal(theta = 0, normal = 0, i_test = 0) :
    """
    Convert theta to normal range
    normal == 0, theta --> (0, 2*pi] (default)
    normal == 1, theta --> (-pi, pi]
    theta = theta0 + k*2*pi
    chunan@ipp.ac.cn 2018.06.29
    """
    if i_test == 1 :
        theta = numpy.array([-7.2*pi, 3*pi, -pi, 0*pi, 13.5*pi, 2.001*pi])
    
    # convert float, list type to ndarray type vlaue
    theta = to_ndarray(theta)
    theta0 = numpy.zeros(theta.shape)    
    if normal == 0 :
        k = numpy.ceil(theta/(2*pi)) - 1
        theta0 = theta - k*2*pi
    elif normal == 1 :
        k = numpy.ceil(theta/(2*pi)) - 1
        theta0 = theta - k*2*pi - pi
    
    if i_test == 1 :
        x = numpy.linspace(-0.5, len(theta) - 0.5, 50)
        if normal == 0 :
            theta1 = numpy.ones(x.shape)*0
            theta2 = numpy.ones(x.shape)*2*pi
        elif normal == 1 :
            theta1 = numpy.ones(x.shape)*(-pi)
            theta2 = numpy.ones(x.shape)*pi
            
        pylab.figure()
        pylab.plot(theta*180/pi, '*', color = 'blue', markersize = 9)
        pylab.hold('on')
        pylab.plot(theta0*180/pi, '<', color = 'red', markersize = 9)
        pylab.legend(['theta','theta0'])
        pylab.hold('on')
        pylab.plot(x, theta1*180/pi, '--', x, theta2*180/pi, '--', color = 'red')
        plot_lib.single_plot_paras()
        pylab.show()
        
    return theta0




def angle_circle_diff(theta = 0, i_test = 0) :
    """
    calculate the circular angle difference on an array of angles head to tail
    input angles should be confined in the range (0, 2*pi] or (-pi, pi]
    chunan@ipp.ac.cn 2018.07.04    
    """
    if i_test == 1 :
        theta = numpy.linspace(0, 2*pi*9.0/10, 10)
        
    theta = to_ndarray(theta)
    theta2 = numpy.append(theta[1:len(theta)], theta[0])
    theta1 = theta
    d_theta = angle_diff(theta1 = theta1, theta2 = theta2)
    
    return d_theta




def angle_diff(theta1 = 0, theta2 = 0, i_test = 0) :
    """
    calculate the smaller angle difference between 2 array of angles
    input angles should be confined in the range (0, 2*pi] or (-pi, pi]
    chunan@ipp.ac.cn 2018.07.04
    """
    if i_test == 1 :
        theta1 = -pi/6
        theta2 = pi/6
        
    theta1 = to_ndarray(theta1)
    theta2 = to_ndarray(theta2)
    d_theta = theta2 - theta1
    # find values large than pi and convert them to (-pi, pi]    
    i_large = numpy.where(d_theta > pi)
    d_theta[i_large] = d_theta[i_large] - 2*pi
    # find values small than -pi and convert them to (-pi, pi]
    i_small = numpy.where(d_theta < -pi)
    d_theta[i_small] = d_theta[i_small] + 2*pi
    
    return d_theta




def circle_diff(x = 0, i_test = 0) :
    """
    conduct diff for an array or a matrix include head and tail
    chunan@ipp.ac.cn 2018.06.28
    """
    if i_test == 1 :
        x = numpy.array([1.1, 2.3, 3.1, 4.3, 5.1])
    elif i_test == 2 :
        x = numpy.array([[1.1, 2.3, 3.1, 8], [4, 5, 6, 7], [2, 2, 3, 3.1]])

    x=numpy.array(x)
    y = numpy.zeros(x.shape)
    if len(x.shape) == 1 :
        # dim = 1 array case
        y[0:len(x) - 1] = numpy.diff(x)
        y[len(x) - 1] = x[0] - x[-1]
    elif len(x.shape) >= 2 :
        # dim > 2 matrix case, set diff operation on the 1st dimension (column)
        y[0:x.shape[0] - 1, :] = numpy.diff(x, axis = 0)
        y[x.shape[0] - 1, :] = x[0, :] - x[-1, :]
    
    if i_test > 0 :
        print 'x: ', x
        print 'circle_diff(x): ', y
        
    return y




def sortlist(li = 0, index = 0, i_test = 0) :
    """
    sort a list with index array
    chunan@ipp.ac.cn 2018.06.28    
    """
    if i_test == 1 :
        li = [2, 1, 3]
        index = numpy.array([1, 0, 2])
    new_list = []
    for i in range(0, len(li)) :
        new_list.append(li[index[i]])
    return new_list




def residue(x, basis = 10, i_test = 0) :
    """
    get residue number i for x with basis as n0, where x = n0*N + i
    chunan@ipp.ac.cn 2018.06.13
    """
    if i_test == 1 :
        x = 103
        basis = 10
    N = numpy.round(x/basis)
    i = x - N*basis
    if i_test == 1 :
        print 'x = ', x
        print 'basis = ', basis
        print 'residue = ', i
    return i




def accumulate_integerate(x,y):
    """
    Acumulate integration function
    chunan@ipp.ac.cn 2016/09/15
    """
    length_x=pylab.size(x)
    z=numpy.zeros(length_x)
    dx=x[2]-x[1]
    s=0
    i=0
    while i<length_x:    
        s=s+y[i]*dx
        z[i]=s
        i=i+1
    return z




def curl_3D_cartersian(Ax_array,Ay_array,Az_array,ix,iy,iz):
    """
    do curl operation
    """
    # define the length of the derivation    
    d=0.001
    Bx=(Az_array[ix][iy+1][iz]-Az_array[ix][iy][iz])/d - (Ay_array[ix][iy][iz+1]-Ay_array[ix][iy][iz])/d
    By=Ay_array[ix][iy][iz]
    Bz=0
    return Bx, By, Bz




def diff_1D_element(f,x,i):
    """
    define one dimensional differential operation at a certain point
    """
    f_diff=(f[i+1]-f[i])/(x[i+1]-x[i])
    return f_diff




def diff_1D_array(f,x):
    """
    define one dinmesional differential operation for an array
    """
    dx=x[1]-x[0]
    length_x=numpy.size(x)
    f0=f
    # reduce the length of the string
    f1=f
    f1[0:length_x-2]=f[1:length_x-1]
    f1[length_x-1]=f[0]
    # multiply this 0.1 to convert it to full length float value
    diff_1D_array=(f1*0.1-f0)/dx
    # set the last invaild slope value to zero as well as satisfy the length limitation
    diff_1D_array[length_x-1]=0
    return diff_1D_array




def fft_real_array(t,sig,i_plot=0,i_test=0):
    """
    calcualte real fft transform to a 1D array
    chunan@ipp.ac.cn 2016/10/03
    """
    # ---- generate test signal  
    if i_test==1:
        pylab.close('all')
        t=numpy.linspace(0,2,10000)
        sig=numpy.sin(2*pi*500*t)
    dt=(t[2]-t[0])/2.0
    Fs=1/dt
    sig_fft=numpy.fft.fft(sig)
    sig_fft_abs=numpy.absolute(sig_fft)/len(t)
    # ---- reorder the frequency and take only the positive half
    f_real=numpy.linspace(0,Fs/2,len(t)/2+1)
    sig_fft_real=sig_fft_abs[0:len(t)/2+1]
    if i_plot==1:
        pylab.figure()
        pylab.plot(f_real,sig_fft_real)
        pylab.xlim(f_real[0],f_real[len(f_real)-1])
        pylab.xlabel('f(Hz)')
        pylab.show()  
    # ---- return function values
    return f_real,sig_fft_real




def fft_real_matrix(Fs,sig_2D,i_plot=0,i_test=0):
    """
    calcualte real fft transform to the first dimension of a 2D matrix
    chunan@ipp.ac.cn 2016/10/03
    """
    # ---- generate test data    
    if i_test==1:
        pylab.close('all')
        t=numpy.linspace(0,2,10000)
        sig=numpy.sin(2*pi*500*t)
        sig.shape=[sig.shape[0],1]
        sig_2D=sig*numpy.ones([1,10])
        dt=(t[2]-t[0])/2.0
        Fs=1/dt
        print sig.shape, sig_2D.shape  
    # ---- apply real fft to the first dimension of the matrix
    # pay attention to apply fft to the correct dimension
    length_t = sig_2D.shape[0]
    sig_2D_fft=numpy.fft.fft(sig_2D,axis=0)
    sig_2D_fft_abs=numpy.absolute(sig_2D_fft)
    sig_2D_fft_real=sig_2D_fft_abs[0:length_t/2+1,:]
    # ---- calculate frequency array
    f_real=numpy.linspace(0,Fs/2,length_t/2+1)
    # plot the column array of the 2D signal matrix
    if i_plot==1:  
        pylab.figure()
        pylab.plot(f_real,sig_2D_fft_real[:,0])
        pylab.xlim(f_real[0],f_real[len(f_real)-1])
        pylab.hold('on')
        pylab.plot(f_real,sig_2D_fft_real[:,numpy.round(sig_2D_fft_abs.shape[1]/2)])
        pylab.xlim(f_real[0],f_real[len(f_real)-1])
        pylab.legend(['test1','test2'])
        pylab.xlabel('f(Hz)')
        pylab.show()
    # ---- return values for function
    return f_real, sig_2D_fft_real, sig_2D_fft_abs




def find_time_index(t, t_want, i_plot = 0, i_test = 0):
    """
    Find the index from a time array for a particular time value
    """
    if i_test == 1:
        t = numpy.linspace(-1,1,333)
        t_want = 0.33333
        i_plot = 1
    if t_want < t[0] or t_want > t[len(t) - 1]:
        print 't_want goes out the range of t'
    dt = (t[2] - t[0])/2.0
    i_want = numpy.round((t_want - t[0])/dt)
    if i_plot == 1:
        pylab.close('all')
        x=numpy.arange(0,t.shape[0],1)
        pylab.figure()
        pylab.plot(x,t,color='blue')
        pylab.hold('on')
        pylab.plot(x[i_want],t[i_want],'o',color='red')
        print i_want
    return i_want




def find_time_points(t, t_want, i_plot = 0, i_test = 0):
    """
    Find time index for an array of time points on time array t
    """
    if i_test == 1:
        print 'test data used'
        ind = numpy.linspace(-3, 2.2, 343)
        t = 10**ind
        t_want = numpy.array([9, 0.1, 0.05, 1.732, 12])
        i_plot = 1
    # convert a pure number t_want to a list with length and attribute
    if numpy.isscalar(t_want) :
        # print t_want, 'is a scalar'
        t_want = numpy.array([t_want])
    if numpy.min(t_want) < t[0] or numpy.max(t_want) > t[len(t) - 1] :
        raise Exception('Error: t_want goes out the range of t')
    # sum up the difference of time difference to judge whether it is even.
    dt_sum = numpy.sum(numpy.diff(numpy.diff(t))) 
    if dt_sum < 10**-10 :
        dt = (t[2] - t[0])/2.0
        i_want = (t_want - t[0])/dt
        # convert i_want to python style index that start from 0
        i_want = i_want - 1
    else:
        print 'Sum of ddt: ', dt_sum
        print 'Time array is not even, slow loop method used!'
        i_want = numpy.ones(t_want.shape)*-1
        for i in range(0, len(t_want)) :
            for j in range(0, len(t)) :
                if t_want[i] >= t[j] and t_want[i] < t[j+1] :
                    i_want[i] = j
    # convert index i_want to integers
    i_want = numpy.int_(i_want)
    if i_plot == 1:
        print 't_want: ', t_want
        print 'i_want: ', i_want
        pylab.figure()
        x=numpy.arange(0, t.shape[0], 1)
        pylab.plot(x, t, color = 'blue')
        pylab.hold('on')
        pylab.plot(x[i_want], t[i_want], 'o', color = 'red')
        pylab.xlabel('index')
        pylab.ylabel('time (s)')
    return i_want




def find_multi_values(y_array,y_want,dy):
    """
    find values' index for a function value y
    chunan@ipp.ac.cn 2016/09/15    
    """
    i=0
    while i<=pylab.size(y_want)-1:
        if i==0:
            i_want=numpy.where( (y_array>=y_want[0]-dy)*(y_array<=y_want[0]+dy) )
        else:
            want=numpy.where( (y_array>=y_want[i]-dy)*(y_array<=y_want[i]+dy) )
            i_want=numpy.concatenate((i_want,want),1)
        i=i+1
    if pylab.size(i_want)<=0:
        print  "points not found!"
    return i_want




def arccos_0_2pi(x, y) :
    """
    Extend the value range of arccos() from [0,pi] to [0,2pi]
    With the consideration of the sign of x and y
    input x, y are the displacements of point P to basis point O
    chunan@ipp.ac.cn 2016/10/10
    """
    r = numpy.sqrt(x*x + y*y)
    cos_value = x/r
    if y >= 0 :
        theta = numpy.arccos(cos_value)
    elif y < 0 :
        theta = 2*pi - numpy.arccos(cos_value)
    return theta




def xy2angle(x, y, normal = 0) :
    """
    Extend function arccos_0_2pi() to the case of arrary inputs
    inputs:    
    normal = 0, angle in (0, 2*pi] (default)
    normal = 1, angle in (-pi, pi]
    chunan@ipp.ac.cn 2016/10/10
    """
    x = to_ndarray(x)
    y = to_ndarray(y)   
    arccos_vec = numpy.vectorize(arccos_0_2pi)
    angle = arccos_vec(x, y)
    angle = numpy.array(angle)
    if normal == 1 :
        # map angle from (0, 2*pi] to (-pi, pi]
        i_neg = numpy.where(angle > pi)
        print 'i_neg: ', i_neg
        print 'angle: ', angle        
        angle[i_neg] = angle[i_neg] - 2*pi
    else :
        # keep angle in range (0, 2*pi]
        angle = angle        
    return angle




def to_ndarray(x = 0) :
    """
    Convert pure number int/float and list to ndarray, 
    If x is ndarray, keep its structure unchanged
    chunan@ipp.ac.cn 2018.07.04
    """
    if isinstance(x, int) or isinstance(x, float) :
        x = numpy.array([x])
    elif isinstance(x, list) :
        x = numpy.array(x)
    else :
        x = x
        
    return x