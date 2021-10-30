#!/usr/bin/env python
import os, sys
import argparse

import numpy as np

import ms2840a



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
        nAve = config['nAve']
        nRun = config['nRun']
        filename = filename_prefix+f'_{mode}_{freq_start:.6f}GHz_span{freq_span*1.e-3:.2f}MHz_rbw{rbw:.1f}kHz_{meas_time:.1f}sec_{nAve:d}counts_{nRun:d}runs'
        try:
            ret = ms2840a.main(
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
            [25.,2000], [50.,1000], [100.,500], [250.,200], [500.,100],
            [1.e+3,50], [2.5e+3,20], [5.e+3,10], [10.e+3,5], [31.25e+3,2]]) # [max span(kHz), max time(sec)]
    fft_time_max_spans = fft_time_max[:,0]
    fft_time_max_times = fft_time_max[:,1]
    fft_rbw_min=np.array([
            [50.,1.e-3], [100.,3.e-3], [500.,10.e-3], 
            [1.e+3,0.03], [5.e+3,0.1], [5.e+3,0.1], [31.25e+3,0.3]]) # [max span(kHz), min rbw(kHz)]
    fft_rbw_min_spans = fft_rbw_min[:,0]
    fft_rbw_min_rbws  = fft_rbw_min[:,1]
    fft_rbw_max=np.array([
            [1.,30.e-3], [5.,100.e-3], [10.,300.e-3], 
            [50.,1.], [100.,3.], [500.,10.], 
            [1.e+3,30.], [2.5e+3,100.], [10.e+3,300.], [31.25e+3,1.e+3]]) # [max span(kHz), max rbw(kHz)]
    fft_rbw_max_spans = fft_rbw_max[:,0]
    fft_rbw_max_rbws  = fft_rbw_max[:,1]
    rbw_values = [1.e-3,3.e-3,1.e-2,3.e-2,1.e-1,3.e-1,1.,3.,1.e+1,3.e+1,1.e+2,3.e+2,1.e+3]
    for mode in modes:
        if not mode in ['FFT', 'SWEEP']:
            print(f'create_configs(): Error! There is no mode of {mode}')
            print(f'create_configs(): Error! --> Skip!')
            continue
        for freq_start in freq_starts:
            for freq_span in freq_spans:
                for rbw in rbws:
                    if not (rbw in rbw_values): 
                        print(f'create_configs(): Warning! RBW {rbw} kHz is not in valid rbw values.')
                        print(f'create_configs(): Warning! --> Skip!')
                        continue
                        pass
                    if mode=='FFT':
                        rbw_min = fft_rbw_min_rbws[freq_span<=fft_rbw_min_spans][0]
                        rbw_max = fft_rbw_max_rbws[freq_span>=fft_rbw_max_spans][-1]
                        if not( rbw_min<=rbw and rbw<=rbw_max ):
                            print(f'create_configs(): Warning! RBW {rbw} kHz is not in valid rbw range ({rbw_min}--{rbw_max} kHz) for span {freq_span} kHz.')
                            print(f'create_configs(): Warning! --> Skip!')
                            continue
                        pass
                    for meas_time in meas_times:
                        if mode=='FFT':
                            tmax = fft_time_max_times[freq_span<=fft_time_max_spans][0]
                            if meas_time > tmax:
                                print(f'create_configs(): Warning! Time {meas_time} sec is longer than the maximum record time for span {freq_span} kHz.')
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

    # For 2021/10/29 signal data taking
    outdir = '~/data/ms2840a/signal_data'
    freq_starts = np.arange(26400e+6 - 250e+3, 26500e+6 - 250e+3, 2e+6) # Hz
    freq_spans  = [2.5e+3] # kHz
    rbws = [0.3] # kHz
    meas_times = [10] # sec
    nAves = [1] # times
    nRuns = [12] # times

    # For test
    '''
    outdir = '~/data/ms2840a/signal_data_test'
    freq_starts = np.arange(26400e+6 - 250e+3, 26410e+6 - 250e+3, 2e+6) # Hz
    freq_spans  = [2.5e+3] # kHz
    rbws = [0.3] # kHz
    meas_times = [1] # sec
    nAves = [1] # times
    nRuns = [2] # times
    #'''

    # freq_starts: Hz --> GHz
    print(f'freq_stars [Hz]: {freq_starts}')
    freq_starts = freq_starts *  1.e-9
    print(f'freq_stars [GHz]: {freq_starts}')


    configs = np.array(create_configs(modes, freq_starts, freq_spans, rbws, meas_times, nAves, nRuns))

    print(f'configs (size={len(configs)}):')
    print(configs)
    if run: run_scanpars(configs, noplot=noplot, overwrite=overwrite, shortconfig=shortconfig, filename_prefix=filename_prefix, outdir=outdir)
    pass
