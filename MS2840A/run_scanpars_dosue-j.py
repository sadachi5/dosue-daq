#!/usr/bin/env python
import os, sys
import argparse

import numpy as np

import MS2840A



def run_scanpars(configs, 
        filename_prefix='scan', 
        filename_add_suffix=False, 
        noplot = True, overwrite=False, shortconfig=True,
        outdir = '~/data/ms2840a/scan'):

    for config in configs:
        mode = config['mode']
        freq_start = config['freq_start']
        freq_span = config['freq_span']
        rbw = config['rbw']
        meas_time = config['meas_time']
        print(meas_time, 'sec')
        nAve = config['nAve']
        nRun = config['nRun']
        filename = filename_prefix+f'_{mode}_{freq_start*1e-9:.6f}GHz_span{freq_span*1.e-6:.2f}MHz_rbw{rbw:.0f}Hz_{meas_time:.1f}sec_{nAve:d}counts_{nRun:d}runs'
        try:
            ret = MS2840A.main(
                mode       = mode, 
                freq_start = freq_start,
                freq_span  = freq_span,
                rbw        = rbw,
                meas_time  = meas_time,
                nAve       = nAve,
                nRun       = nRun,
                outdir     = outdir, 
                filename   = filename,
                noplot     = noplot,
                overwrite  = overwrite,
                shortconfig= shortconfig,
                filename_add_suffix = filename_add_suffix)
        except Exception as e:
            print(f'run_scanpars(): Error! {e} for {filename}')
            print(f'run_scanpars(): Error! --> skip!')
            continue
        pass

    return 0

def create_configs(modes, freq_starts, freq_spans, rbws, meas_times, nAves, nRuns):
    configs = []
    fft_time_max=np.array([
            [25.e+3,2000], [50.e+3,1000], [100.e+3,500], [250.e+3,200], [500.e+3,100],
            [1.e+6,50], [2.5e+6,20], [5.e+6,10], [10.e+6,5], [31.25e+6,2]]) # [max span(Hz), max time(sec)]
    fft_time_max_spans = fft_time_max[:,0]
    fft_time_max_times = fft_time_max[:,1]
    fft_rbw_min=np.array([
            [50.e+3,1.], [100.e+3,3.], [500.e+3,10.], 
            [1.e+6,30.], [5.e+6,100.], [5.e+6,100.], [31.25e+6,300.]]) # [max span(Hz), min rbw(Hz)]
    fft_rbw_min_spans = fft_rbw_min[:,0]
    fft_rbw_min_rbws  = fft_rbw_min[:,1]
    fft_rbw_max=np.array([
            [1.e+3,30.], [5.e+3,100.], [10.e+3,300.], 
            [50.e+3,1000.], [100.e+3,3000.], [500.e+3,10.e+3], 
            [1.e+6,30.e+3], [2.5e+6,100.e+3], [10.e+6,300.e+3], [31.25e+6,1.e+6]]) # [max span(Hz), max rbw(Hz)]
    fft_rbw_max_spans = fft_rbw_max[:,0]
    fft_rbw_max_rbws  = fft_rbw_max[:,1]
    rbw_values = [1.,3.,10.,30.,100.,300.,1.e+3,3.e+3,1.e+4,3.e+4,1.e+5,3.e+5,1.e+6]
    for mode in modes:
        if not mode in ['FFT', 'SWEEP']:
            print(f'create_configs(): Error! There is no mode of {mode}')
            print(f'create_configs(): Error! --> Skip!')
            continue
        for freq_start in freq_starts:
            for freq_span in freq_spans:
                for rbw in rbws:
                    if not (rbw in rbw_values): 
                        print(f'create_configs(): Warning! RBW {rbw} Hz is not in valid rbw values.')
                        print(f'create_configs(): Warning! --> Skip!')
                        continue
                        pass
                    if mode=='FFT':
                        rbw_min = fft_rbw_min_rbws[freq_span<=fft_rbw_min_spans][0]
                        rbw_max = fft_rbw_max_rbws[freq_span>=fft_rbw_max_spans][-1]
                        if not( rbw_min<=rbw and rbw<=rbw_max ):
                            print(f'create_configs(): Warning! RBW {rbw} Hz is not in valid rbw range ({rbw_min}--{rbw_max} Hz) for span {freq_span} Hz.')
                            print(f'create_configs(): Warning! --> Skip!')
                            continue
                        pass
                    for meas_time in meas_times:
                        if mode=='FFT':
                            tmax = fft_time_max_times[freq_span<=fft_time_max_spans][0]
                            if meas_time > tmax:
                                print(f'create_configs(): Warning! Time {meas_time} sec is longer than the maximum record time for span {freq_span} Hz.')
                                print(f'create_configs(): Warning! --> Skip!')
                                continue
                            pass
                        for nAve in nAves:
                            for nRun in nRuns:
                                config = {
                                        'mode':mode, 
                                        'freq_start':freq_start, 
                                        'freq_span':freq_span, 
                                        'rbw':rbw, 
                                        'meas_time':meas_time, 
                                        'nAve':nAve, 
                                        'nRun':nRun
                                        }
                                configs.append(config)
                                pass
                            pass
                        pass
                    pass
                pass
            pass
        pass
    return configs
if __name__=='__main__':
    # Global settings
    filename_prefix = 'scan'
    noplot = True
    overwrite = False
    shortconfig = True
    run = True

    # Scan parameters
    modes = ['FFT'] # FFT or SWEEP


    # For 2022/10/21 signal data taking test
    '''
    outdir = '~/data/ms2840a/dosue-j/test'
    freq_starts = np.arange(14000e+6 - 250e+3, 14001e+6 - 250e+3, 2e+6) # Hz
    freq_spans  = [2.5e+6] # Hz
    rbws = [300] # Hz
    # meas_times = [2] # sec
    meas_times = [1] #sec
    nAves = [1] # times
    # nRuns = [12] # times
    nRuns = [1] # times
    #'''

    # 本番 22/10/21
    #'''
    freq_starts = np.arange(14100e+6 - 250e+3, 14200e+6 - 250e+3, 2e+6) # Hz
    freq_spans  = [2.5e+6] # Hz
    rbws = [300] # Hz
    nAves = [1] # times
    #'''

    # Dark photon search
    '''
    outdir = '~/data/ms2840a/dosue-j/signal_data'
    meas_times = [2] # sec
    nRuns = [12] # times
    #'''
    # Y-factor
    #'''
    outdir = '~/data/ms2840a/dosue-j/yfactor_300K_ini' # 300K before measurement
    #outdir = '~/data/ms2840a/dosue-j/yfactor_77K_ini' # 77K before measurement
    #outdir = '~/data/ms2840a/dosue-j/yfactor_300K_fin' # 300K after measurement
    #outdir = '~/data/ms2840a/dosue-j/yfactor_77K_fin' # 77K after measurement
    meas_times = [1] # sec
    nRuns = [1] # times
    #'''
    
    # freq_starts: Hz --> GHz
    print(f'freq_stars [Hz]: {freq_starts}')

    configs = np.array(create_configs(modes, freq_starts, freq_spans, rbws, meas_times, nAves, nRuns))

    print(f'configs (size={len(configs)}):')
    print(configs)
    if run: run_scanpars(configs, noplot=noplot, overwrite=overwrite, shortconfig=shortconfig, filename_prefix=filename_prefix, outdir=outdir)
    pass
