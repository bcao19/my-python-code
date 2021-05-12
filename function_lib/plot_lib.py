"""
plot_lib.py module to define some useful plot functions
chunan@ipp.ac.cn 2018.06.29
"""
import pylab
import numpy




def axes_equal_3d(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    copied codes from internet 
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = numpy.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = numpy.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = numpy.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])




def single_plot_paras(fontsize = 15, i_test = 0, numpoints = 1) :
    """parameters for a single plot"""
    if i_test == 1 :
        x = numpy.linspace(0, 1, 30)
        y = numpy.sin(x)
        pylab.figure()
        pylab.plot(x, y, '*')
        pylab.legend(['test',])
        pylab.xlabel('x label')
        pylab.ylabel('y label')
        pylab.title('test plot')

    pylab.rcParams['legend.numpoints'] = numpoints
    pylab.rcParams.update({'font.size': fontsize})
    pylab.grid('on')
    pylab.minorticks_on()
    pylab.tick_params(which = 'major', labelsize = fontsize, width = 2, 
                      length = 10, color = 'black')
    pylab.tick_params(which = 'minor', width = 1, length = 5)
    pylab.tight_layout()

    if i_test == 1 :
        pylab.show()



    
def single_axis_paras(ax, fontsize = 15, numpoints = 1) :
    """parameters for a paticular axis"""
    pylab.rcParams['legend.numpoints'] = numpoints
    pylab.rcParams.update({'font.size': fontsize})
    ax.grid('on')
    ax.minorticks_on()
    ax.tick_params(which = 'major', labelsize = fontsize, width = 2, length = 10)
    ax.tick_params(which = 'minor', width = 1, length = 5)




# parameters for a single plot
def yyplot(x1, y1, x2, y2, ylab1= '', ylab2 = '', color1='blue', 
           color2='red', fontsize=15, linewidth=1.5) :
    # acquire two axes
    ax1=pylab.gca()
    ax2=ax1.twinx()
    # plot y1,y2 signals
    ax1.plot(x1,y1,color=color1,linewidth=linewidth)
    ax2.plot(x2,y2,color=color2,linewidth=linewidth)
    # set label colors
    ax1.set_ylabel(ylab1,fontsize=fontsize,color=color1)
    ax2.set_ylabel(ylab2,fontsize=fontsize,color=color2)
    # set axis boarder colors
    ax2.spines['left'].set_color(color1) 
    ax2.spines['right'].set_color(color2)
    # set tick marker and label colors
    ax1.tick_params(axis='y',colors=color1)
    ax2.tick_params(axis='y',colors=color2)
    # set minor tick colors
    ax1.tick_params(which='minor',axis='y',color=color1)
    ax2.tick_params(which='minor',axis='y',color=color2)   
    # set default parameters
    single_axis_paras(ax1)
    single_axis_paras(ax2)
    return ax1,ax2


def subaxes_N1(ax = 0, names = 0, EDx = 0.08, EDy = 0.08, i_test = 0) :
    """This function takes in a dic containing axes of a subplot"""
    if i_test == 1 :
        pylab.figure(figsize = (6, 8))
        axes = {}
        x = numpy.linspace(0, 1, 10)
        names = ['ax0', 'ax1', 'ax2', 'ax3', 'ax4']
        for i in range(0, len(names)) :
            axes[names[i]] = pylab.subplot(len(names), 1, i + 1)
            axes[names[i]].plot(x, numpy.sin(2*i*x))
            pylab.legend([names[i],])
        ax = axes
        
    ax_item = ax.items()
    n_fig = len(ax_item)
    dx = 1 - 2*EDx
    dy = (1.0 - 2*EDy)/n_fig
    for i in range(0, n_fig) :
        ax[names[i]].set_position([EDx, 1 - EDy - (i + 1)*dy, dx, dy])
        single_axis_paras(ax[names[i]])
        if i <= n_fig - 2 :
            pylab.setp(ax[names[i]].get_xticklabels(), visible=False)


