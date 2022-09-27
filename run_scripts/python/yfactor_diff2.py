#!/bin/env python3
import os
import sys
import argparse
import csv
import numpy as np
from matplotlib import pyplot as plt

# set colorful lines
cmap = plt.get_cmap('jet')

# start_freq, stop_freq, npoints are only used in OneColumn type
def read_csv(filename, csvType='Anritsu', start_freq=None, stop_freq=None, npoints=None):
    
    freq = [] # frequency list [GHz]
    power = [] # power list  [mW]
    
    f = open(filename, 'r');
    if csvType=='TwoColumn':
        fin = list( csv.reader(f, delimiter=' ') )
    else:
        fin = list(csv.reader(f))
    #print(fin)  #リストの中身を出力
    isData = False
    
    if csvType=='Anritsu': # Anritsu : NOTE: only for RMS detection
        
        start_freq = 0
        stop_freq = 0
        npoints = 0
        for line in fin:
            if len(line)==0 : continue
            first = line[0].strip()
            # Search for frequency range
            if first == 'Trace-A':
                start_freq = int(line[1])
                stop_freq  = int(line[2])
                continue
            # Search for npoints
            if first == 'RMS':
                npoints = int(line[1])
                continue
            # Search for data starting point (Anritsu: Wave Data)
            if first.startswith('Wave Data'):
                isData = True
                continue
            # Get data
            if isData:
                power.append(10 ** (float(line[0])*0.1)) # dBm --> mW
                pass
            pass
        freq = np.linspace(start_freq,stop_freq,npoints) * 1.e-9 # Hz --> GHz
            
    elif csvType=='Keysight' : # Keysight
        
        for line in fin:
            if len(line)==0 : continue
            # Search for data starting point (Keysight: DATA)
            #print(f'first = {first}')
            if first == 'DATA':
                isData = True
                continue
            isData = True # All lines are data
            # Get data
            if isData:
                freq.append( float(line[0]) * 1.e-9 ) # Hz --> GHz
                power.append(10 ** (float(line[1])*0.1)) # dBm --> mW
                pass
            pass
        
    elif csvType=='TwoColumn' : # Hz, dBm
        
        for line in fin:
            if len(line)==0 : continue
            first = line[0].strip()
            #print(f'first = {first}')
            if first[0]=='#':
                # skip line
                continue
            # Get data
            freq.append( float(line[0]) * 1.e-9 ) # Hz --> GHz
            power.append(10 ** (float(line[1])*0.1)) # dBm --> mW
            pass
        
    elif csvType=='OneColumn' : # dBm
        
        for line in fin:
            if len(line)==0 : continue
            first = line[0].strip()
            #print(f'first = {first}')
            if first[0]=='#':
                # skip line
                continue
            # Get data
            power.append(10 ** (float(line[0])*0.1)) # dBm --> mW
            pass
        if (start_freq is None) or (stop_freq is None) or (npoints is None):
            print('Error! There is no arguments for frequency information (start_freq, stop_freq, npoints).')
            print('Error! Please specify them!')
            return None
        freq = np.linspace(start_freq,stop_freq,npoints) * 1.e-9 # Hz --> GHz
        
        pass
    
    return np.array(freq), np.array(power)
                
def read_average(filenames, csvType):
    freq = []
    power_sum = []
    for i, _file in enumerate(filenames):
        _freq, _power = read_csv(f'{_file}', csvType)
        if i == 0:
            freq = _freq
            power_sum = _power
        else:
            power_sum += _power
            pass
    power_ave = power_sum / len(filenames)
    return freq, power_ave

def freq_average(data, naverage=100):

    ndata = len(data)
    npoints = int(ndata/naverage)
    
    data_ave = []
    data_err = []
    
    for i in range(npoints):
        data_subset = data[i*naverage:(i+1)*naverage]
        average = np.mean(data_subset)
        average_err = np.std(data_subset)/np.sqrt(naverage) #  = 1/N * sqrt( sum((y-mean)^2))  ( std = sqrt( sum((y-mean)^2) / N) )
        data_ave.append(average)
        data_err.append(average_err)
        pass
    
    return np.array(data_ave), np.array(data_err)


def main(outdir, outname, input1, input2, nRun1=1, nRun2=1):
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
        pass
    label_1 = '300K'
    label_2 = '77K'
    csvType_1 = 'TwoColumn'; # freq, dBm
    csvType_2 = 'TwoColumn'; # freq, dBm

    freq_min = 4. # [GHz]
    freq_max = 12 # [GHz]

    input_list1 = [ f'{input1}_{i}.dat' for i in range(nRun1) ]
    input_list2 = [ f'{input2}_{i}.dat' for i in range(nRun2) ]
    freq_1, power_1 = read_average(input_list1, csvType_1)
    freq_2, power_2 = read_average(input_list2, csvType_2)

    # Select data between freq_min and freq_max
    power_1 = power_1[freq_1<=freq_max]
    freq_1 = freq_1[freq_1<=freq_max]
    power_1 = power_1[freq_1>=freq_min]
    freq_1 = freq_1[freq_1>=freq_min]
    power_2 = power_2[freq_2<=freq_max]
    freq_2 = freq_2[freq_2<=freq_max]
    power_2 = power_2[freq_2>=freq_min]
    freq_2 = freq_2[freq_2>=freq_min]
    
    # Averaging
    nAve = 50
    freq_1_ave, tmp = freq_average(freq_1, naverage=nAve)
    freq_2_ave, tmp = freq_average(freq_2, naverage=nAve)
    power_1_ave, power_1_ave_err = freq_average(power_1, naverage=nAve)
    power_2_ave, power_2_ave_err = freq_average(power_2, naverage=nAve)

    power_diff = power_1/power_2
    power_diff_ave = power_1_ave/power_2_ave
    power_diff_dB = np.log10(power_diff)*10.
    power_diff_ave_dB = np.log10(power_diff_ave)*10.

    # Exclude 5--6 GHz to avoid Wifi
    power_1_mod = power_1[(freq_1<5.) | (freq_1>6.)]
    power_2_mod = power_2[(freq_2<5.) | (freq_2>6.)]
    total_power_diff_ave = np.sum(power_1_mod)/np.sum(power_2_mod)
    total_power_diff_ave_dB = np.log10(total_power_diff_ave)*10.

    n_freq = len(freq_1_ave)
    n_half = (int)(n_freq/2)
    print(f'y-factor = {power_diff_ave_dB[n_half]} @ {freq_1_ave[n_half]} GHz')
    print(f'y-factor = {total_power_diff_ave_dB} (averaged power from {freq_min}--{freq_max} GHz excluding 5--6 GHz)')

    plt.rcParams["font.size"] = 16
    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.labelsize"] = 16
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16

    fig, axs = plt.subplots(2,1)
    fig.set_size_inches(12,12)
    fig.tight_layout();
    plt.subplots_adjust(wspace=0.05, hspace=0.2, left=0.10, right=0.95,bottom=0.10, top=0.90)

    ax = axs[0]
    ax.plot(freq_1, power_1, label=f'{label_1}', color='blue', marker='o', markersize=0.5, linestyle='', linewidth=0.)
    ax.plot(freq_2, power_2, label=f'{label_2}', color='red', marker='o', markersize=0.5, linestyle='', linewidth=0.)
    ax.plot(freq_1_ave, power_1_ave, label=f'{label_1} rebin', color='blue', marker='', markersize=0.5, linestyle='-', linewidth=2)
    ax.plot(freq_2_ave, power_2_ave, label=f'{label_2} rebin', color='red', marker='', markersize=0.5, linestyle='-', linewidth=2)
    ax.set_xlabel('Frequency [GHz]') #x軸の名前
    ax.set_ylabel('Power [mW]') #y軸の名前

    ax = axs[1]
    
    ax.plot(freq_1, power_diff_dB, label=f'{label_1}/{label_2}', color='blue', marker='o', markersize=0.5, linestyle='', linewidth=0)
    ax.plot(freq_1_ave, power_diff_ave_dB, label=f'{label_1}/{label_2} rebin', color='blue', marker='', markersize=0.5, linestyle='-', linewidth=2)
    ax.set_xlabel('Frequency [GHz]') #x軸の名前
    ax.set_ylabel('Difference ratio [dB]') #y軸の名前

    fig.savefig(f'{outdir}/{outname}')
    return 0


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--outdir', dest='outdir', type=str, default='aho', 
        help=f'output directory (default: aho)')
    parser.add_argument('--outname', dest='outname', type=str, default='aho.pdf', 
        help=f'output file name (default: aho.pdf)')
    parser.add_argument('--input1', dest='input1', type=str,
        help=f'input data file path for 300K')
    parser.add_argument('--input2', dest='input2', type=str,
        help=f'input data file path for 77K')
    parser.add_argument('--nRun1', dest='nRun1', type=int,
        help=f'number of input data files for 300K')
    parser.add_argument('--nRun2', dest='nRun2', type=int,
        help=f'number of input data files for 77K')
    args = parser.parse_args()

    main(
        outdir = args.outdir,
        outname = args.outname,
        input1 = args.input1,
        input2 = args.input2,
        nRun1 = args.nRun1,
        nRun2 = args.nRun2,
    )

    pass
    
