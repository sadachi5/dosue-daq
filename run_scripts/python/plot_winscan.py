#!/bin/env python3
from utils import *
from integral2Dgauss import *
from LMfit import *

def winscan_calculate(
        x_min = -40.*mm, x_max=40.*mm, 
        r_min = 0., r_max = 40.*mm, 
        dx = 1.*mm, dy = 1.*mm,
        L = 100.*mm, HPBW_theta=deg2rad(5.),
        scan_dx = 10.*mm
        ):

    x_list = np.arange(x_min, x_max+scan_dx, scan_dx)
    y_min = -r_max
    y_max = r_max

    def calculate(x_max):
        integral = integral2Dgauss(
            x_min=x_min, x_max=x_max,
            y_min=y_min, y_max=y_max,
            r_min=r_min, r_max=r_max,
            dx=dx, dy=dy, L=L, HPBW_theta=HPBW_theta, verbose=-1)
        return integral

    z_list = [ calculate(x) for x in x_list ]
    z_list = np.array(z_list)
    print(f'calculate z (ratio to max.) = {z_list/z_list[-1]}')
    return x_list, z_list

def integral2DgaussForXmaxFit(
    x_min, x_max, r_min, r_max, 
    dx, dy, L, HPBW_theta,
    verbose=-1):
    x_list = np.arange(x_min, x_max+dx, dx)
    x1 = x_list[-1] if len(x_list)>0 else x_min
    x2 = x1 + dx
    y1 = integral2Dgauss(
        x_min=x_min, x_max=x1, r_min=r_min, r_max=r_max, 
        dx=dx, dy=dy, L=L, HPBW_theta = HPBW_theta,
        verbose=verbose)
    y2 = integral2Dgauss(
        x_min=x_min, x_max=x2, r_min=r_min, r_max=r_max, 
        dx=dx, dy=dy, L=L, HPBW_theta = HPBW_theta,
        verbose=verbose)
    y = y2 * (x_max - x1)/(dx) + y1 * (x2 - x_max)/(dx)
    return y

def fit_integral2Dgauss(
        xdata, ydata, xerr, yerr, r_max=40.*mm,
        dx = 1.*mm, dy = 1.*mm,
        L = 100.*mm
    ):

    def fitfunc(x, par0, par1):
        max_y = integral2DgaussForXmaxFit(
            x_min=-r_max, x_max=r_max, r_min=0., r_max=r_max, 
            dx=dx, dy=dy, L=L, HPBW_theta = deg2rad(par1),
            verbose=-1)
        #print('par0', par0, 'par1', par1, 'max_y', max_y)
        if isinstance( x, (list, np.ndarray) ):
            y = [ integral2DgaussForXmaxFit(
                    x_min=-r_max, x_max=_x-par0*mm, r_min=0., r_max=r_max, 
                    dx=dx, dy=dy, L=L, HPBW_theta = deg2rad(par1),
                    verbose=-1)
                    for _x in x ]
            y = np.array(y)
        else:
            y = integral2DgaussForXmaxFit(
                    x_min=-r_max, x_max=x-par0*mm, r_min=0., r_max=r_max, 
                    dx=dx, dy=dy, L=L, HPBW_theta = deg2rad(par1),
                    verbose=-1)
            pass
        if max_y > 0.:
            y_ratio = y/max_y
        else:
            y_ratio = 0.
            pass
        #print('y_ratio', y_ratio)
        return y_ratio

    init_pars = [45., 25.]
    limit_pars = [[0., 2.*r_max/mm], [0., 100.]] # par0 [mm], par1[deg]
    fix_pars = [False, False]
    
    fit = LMfit(fitfunc, init=init_pars, fix=fix_pars, limit=limit_pars, verbosity=2)
    result = fit.dofit(xdata, ydata, yerr, xerr)
    print('result.chisquare = {}'.format(result.chisqr))
    print('result.params = {}'.format(result.params))
    result_pars = []
    for key, par in result.params.items() :
        print('result.params[{}] = {}'.format(key, par))
        print('result.params[{}] = {}'.format(key, par.value))
        print('result.params[{}] = {}'.format(key, par.stderr))
        result_pars.append(par)
        pass

    print(xdata)
    print(ydata)
    fit_ydata = fitfunc(xdata, result_pars[0], result_pars[1])

    '''
    plt.plot(xdata/mm, ydata, c='k', marker='o', markersize=10, ls='')
    plt.plot(xdata/mm, fit_ydata, c='b', marker='o', markersize=10, ls='')
    plt.savefig('aho.pdf')
    '''
    return result.redchi, result_pars, fit_ydata

def plot_winscan(
        file_list, labels, values, nRun,
        outdir, outname, 
        ymin=None, ymax=None, ylog=False):
    # Configurations
    csvType = 'TwoColumn'; # freq, dBm
    freq_min = 4. # [GHz]
    freq_max = 12 # [GHz]
    nAve = 50 # frequency averaging

    # Check & create the output directory
    check_dir(outdir)

    # Containers
    freq_list = []
    power_list = []
    power_dBm_list = []
    meanPower_list = []
    for _file in file_list:
        # Get input data
        _input_list = [ f'{_file}_{i}.dat' for i in range(nRun) ]
        _freq, _power = read_average(_input_list, csvType)
        # Frequency cut
        _freq, _power = freq_cut(_freq, _power, freq_min, freq_max)
        # Frequency averaging
        _freq_ave, tmp = freq_average(_freq, naverage=nAve)
        _power_ave, tmp = freq_average(_power, naverage=nAve)

        # Calculate mean power excluding 5--6 GHz
        _power_ave_mod = _power_ave[ (_freq_ave<5.) | (_freq_ave>6.) ]
        _meanPower = np.mean(_power_ave_mod)

        # Fill containers
        freq_list.append(_freq_ave)
        power_list.append(_power_ave)
        power_dBm_list.append(mW2dBm(_power_ave))
        meanPower_list.append(_meanPower)
        pass

    # List --> array
    freq_list = np.array(freq_list)
    power_list = np.array(power_list)
    power_dBm_list = np.array(power_dBm_list)
    meanPower_list = np.array(meanPower_list)
    values = np.array(values)

    # Prepare a figure
    default_figure()
    fig, axs = plt.subplots(3,1)
    fig.set_size_inches(15,12)
    fig.tight_layout();
    plt.subplots_adjust(
            wspace=0.05, hspace=0.30, 
            left=0.10, right=0.95,
            bottom=0.10, top=0.95)

    # Plot each powers
    ax = axs[0]
    for i, _label in enumerate(labels):
        _freq = freq_list[i]
        _power = power_list[i]
        _meanPower = meanPower_list[i]

        ax.plot(_freq, _power, label=f'{_label}: {_meanPower:.2e} mW', linestyle='-', linewidth=2.)
        pass
    default_legend(ax)
    ax.set_xlabel('Frequency [GHz]')
    ax.set_ylabel('Power [mW]')
    if ymin is not None: ax.set_ylim(ymin = ymin)
    if ymax is not None: ax.set_ylim(ymax = ymax)
    if ylog: ax.set_yscale('log')

    # Plot value v.s. mean power
    ax = axs[1]
    ax.plot(values, meanPower_list, linestyle='', marker='o', markersize=10)
    ax.set_xlabel('300K cover length [cm]')
    ax.set_ylabel('Power [mW]')

    # Calculate mean power ratio
    minPower = min(meanPower_list)
    maxPower = max(meanPower_list)
    meanPowerRatio_list = (meanPower_list - minPower)/(maxPower - minPower)
    # Assign error
    values_err = np.full(len(values), 1) # error 1 mm
    meanPowerRatio_err = ( np.abs(meanPowerRatio_list[0]-meanPowerRatio_list[1]) \
            + np.abs(meanPowerRatio_list[-1]-meanPowerRatio_list[-2]) )/2.
    meanPowerRatios_err = np.full(len(values), meanPowerRatio_err)

    # Plot value v.s. mean power
    ax = axs[2]
    ax.errorbar(values, meanPowerRatio_list, xerr=values_err, yerr=meanPowerRatios_err,
            linestyle='', marker='o', markersize=3, color='k')
    ax.set_xlabel('300K cover length [mm]')
    ax.set_ylabel('Power Ratio\n(power - min)/(max - min)')

    # 84.05 mm is from antenna aperture to top surface of the window rim.
    #x_calc, y_calc = winscan_calculate(HPBW_theta=deg2rad(20.), L=84.05*mm) 
    #ax.plot(x_calc/mm+45., y_calc/max(y_calc), linestyle=':', marker='o', markersize=3, color='red')

    # Fit
    fit_redchi, fit_pars, fit_ydata = fit_integral2Dgauss(
        xdata=values*mm, ydata=meanPowerRatio_list,
        xerr=values_err*mm, yerr=meanPowerRatios_err,  
        #xerr=None, yerr=meanPowerRatios_err,  
        r_max=40.*mm, dx = 0.1*mm, dy = 0.1*mm, L = 84.05*mm
    )
    ax.plot(values, fit_ydata, color='r',
            linestyle=':', marker='o', markersize=5)
    ax.text(0., 0.5, f"$\chi^2$/ndof = {fit_redchi}\n\
            x0   = {fit_pars[0].value:.2f} +- {fit_pars[0].stderr:.2f} mm\n\
            HPBW = {fit_pars[1].value:.2f} +- {fit_pars[1].stderr:.2f} deg")

    # Save the figure
    fig.savefig(f'{outdir}/{outname}')
    plt.clf()
    plt.close()

    return 0


if __name__ == '__main__':
    indate = '2022-10-03'
    indir = f'/data/ms2840a/{indate}/data'
    suffix = 'WinScan2'
    prefix = f'DOSUE-Y_test_230GHz_{suffix}-'
    input_labels = ['all', '8cm', '7cm', '6cm', '5cm', '4cm', '3cm', '2cm', '1cm', '0cm', 'no']
    input_values = [100, 80, 70, 60, 50, 40, 30, 20, 10, 0, -20] # [mm]
    nRun = 10
    outdir = f'/data/ms2840a/{indate}/figure'
    outname = f'DOSUE-Y_test_230GHz_{suffix}.pdf'

    ymin = 0.
    ymax = 0.5e-5
    ylog = False

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--outdir', dest='outdir', type=str, default=outdir, 
        help=f'output directory (default: {outdir})')
    parser.add_argument('--outname', dest='outname', type=str, default=outname, 
        help=f'output file name (default: {outname})')
    parser.add_argument('--indir', dest='indir', type=str, default=indir,
        help=f'input directory (default: {indir})')
    parser.add_argument('--prefix', dest='prefix', type=str, default=prefix,
        help=f'input file prefix (default: {prefix})')
    parser.add_argument('--input_labels', dest='labels', 
       nargs='*', type=str, default=input_labels,
        help=f'input file labels (default: {input_labels})')
    parser.add_argument('--input_values', dest='values', 
       nargs='*', type=float, default=input_values,
        help=f'corresponding values for each input file labels (default: {input_values})')
    parser.add_argument('--nRun', dest='nRun', type=int, default=nRun,
        help=f'input data nRun (# of data files for each measurement) (default: {nRun})')
    parser.add_argument('--ymin', dest='ymin', type=float, default=ymin,
        help=f'y-axis min (default: {ymin})')
    parser.add_argument('--ymax', dest='ymax', type=float, default=ymax,
        help=f'y-axis max (default: {ymax})')
    parser.add_argument('--ylog', dest='ylog', action='store_true', default=ylog,
        help=f'y-axis log (default: {ylog})')
    args = parser.parse_args()
    
    file_list = []
    for _label in args.labels:
        _filename = f'{args.indir}/{args.prefix}{_label}'
        file_list.append(_filename)
        pass

    plot_winscan(
            file_list = file_list,
            labels = args.labels,
            values = args.values,
            nRun = args.nRun,
            outdir = args.outdir,
            outname = args.outname,
            ymin = args.ymin,
            ymax = args.ymax,
            ylog = args.ylog,
            )
    pass

