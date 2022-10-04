#!/bin/env python3
import os
import sys
import argparse
import csv
import numpy as np
from matplotlib import pyplot as plt
# set colorful lines
cmap = plt.get_cmap('tab20')


# Import my functions
import get_file_maxindex


# Directory check
def check_dir(dirpath):
    if not os.path.isdir(dirpath):
        print(f'Warning!: There is no directory: {dirpath}.')
        print(f'Warning!: --> Create the directory.')
        os.makedirs(dirpath)
    else:
        print(f'The directory {dirpath} already exists.')
        pass
    return 0


# start_freq, stop_freq, npoints are only used in OneColumn type
# return y-factor_dB, y-factor_dB_at_freq, freq
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
                

def read_average(filenames, csvType='TwoColumn'):
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

def read_average_nRun(
        filepath, nRun=10, suffix='.dat', csvType='TwoColumn'):
    file_list = [ f'{filepath}_{i}{suffix}' for i in range(nRun) ]
    freq, power = read_average(file_list, csvType)
    return freq, power

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


def freq_cut(freq, power, freq_min=None, freq_max=None):
    _freq = np.array(freq)
    _power = np.array(power)
    if freq_max is not None and freq_min is not None:
        new_power = _power[ (_freq >= freq_min) & (_freq <= freq_max) ]
        new_freq = _freq[ (_freq >= freq_min) & (_freq <= freq_max) ]
    elif freq_max is not None:
        new_power = _power[ (_freq <= freq_max) ]
        new_freq = _freq[ (_freq <= freq_max) ]
    else :
        new_power = _power[ (_freq >= freq_min) ]
        new_freq = _freq[ (_freq >= freq_min) ]
        pass
    return new_freq, new_power


def scale2dB(scale):
    return np.log10( scale ) * 10. # scale --> dB

def dB2scale(dB):
    return 10.**(dB*0.1) # dB --> scale

def mW2dBm(mW):
    return scale2dB( mW.astype(np.float64) ) # mW --> dBm

def dBm2mW(dBm):
    return dB2scale( dBm.astype(np.float64) ) # dBm --> mW

def Y2Trx(Y, T_300K=290., T_77K=77.3): # Y[scale] --> Trx[K]
    return (T_300K - Y*T_77K)/(Y-1.)

def YdB2Trx(YdB, T_300K=290., T_77K=77.3): # Y[dB] --> Trx[K]
    Y = dB2Ratio(YdB)
    return Y2Trx(Y, T_300K, T_77K)

def deg2rad(deg):
    return deg*np.pi/180.

def rad2deg(rad):
    return rad*180./np.pi

def default_figure():
    plt.rcParams["font.size"] = 16
    plt.rcParams["axes.grid"] = True
    plt.rcParams["axes.labelsize"] = 16
    plt.rcParams["xtick.labelsize"] = 16
    plt.rcParams["ytick.labelsize"] = 16
    return 0

def default_legend(ax, 
        fontsize=10, title='',
        frameon=False, ncol=1):
    ax.legend(
            fontsize = fontsize, 
            title = title,
            frameon = frameon,
            ncol = ncol,
            )
    return 0


import inspect;
def get_var_name(var, back_vars=None):
    name = ''
    if back_vars==None : 
        back_vars = inspect.currentframe().f_back.f_globals
        back_vars.update(inspect.currentframe().f_back.f_globals)
        pass
    for k,v in back_vars.items():
        if id(v) == id(var):
            name=k
            pass
        pass
    return name
