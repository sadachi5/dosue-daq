#!/bin/env python3
from utils import *

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

    # Plot value v.s. mean power
    minPower = min(meanPower_list)
    maxPower = max(meanPower_list)
    meanPowerRatio_list = (meanPower_list - minPower)/(maxPower - minPower)
    ax = axs[2]
    ax.plot(values, meanPowerRatio_list, linestyle='', marker='o', markersize=10)
    ax.set_xlabel('300K cover length [cm]')
    ax.set_ylabel('Power Ratio\n(power - min)/(max - min)')

    # Save the figure
    fig.savefig(f'{outdir}/{outname}')
    plt.clf()
    plt.close()

    return 0


if __name__ == '__main__':
    indir = '/data/ms2840a/2022-10-03/data'
    prefix = 'DOSUE-Y_test_230GHz_WinScan-'
    input_labels = ['all', '8cm', '7cm', '6cm', '5cm', '4cm', '3cm', '2cm', '1cm', '0cm', 'no']
    input_values = [10, 8, 7, 6, 5, 4, 3, 2, 1, 0, -2]
    nRun = 10
    ymin = 0.
    ymax = 0.5e-5
    ylog = False

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--outdir', dest='outdir', type=str, default='aho', 
        help=f'output directory (default: aho)')
    parser.add_argument('--outname', dest='outname', type=str, default='aho.pdf', 
        help=f'output file name (default: aho.pdf)')
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

