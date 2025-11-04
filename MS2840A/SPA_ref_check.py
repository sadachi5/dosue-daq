# dosue-preY による 7.95 GHz 近傍 (2.5 MHz 帯域) の測定に使用した python script である

#!/usr/bin/env python
import os, sys
import argparse
import numpy as np
import MS2840A


def run_scanpars(configs,
        filename_prefix='scan',
        filename_add_suffix=False,
        noplot=True, overwrite=False, shortconfig=True,
        nosubdir=True, noRun=False,
        outdir='~/data/ms2840a/scan'):

    mode0 = None
    freq_start0 = None
    freq_span0 = None
    rbw0 = None
    meas_time0 = None
    nAve0 = None
    nRun0 = None
    for i, config in enumerate(configs):
        print(f'########## Starting measurement ({i+1}/{len(configs)}) ##########')
        mode = config['mode']
        freq_start = config['freq_start']
        freq_span = config['freq_span']
        rbw = config['rbw']
        meas_time = config['meas_time']
        nAve = config['nAve']
        nRun = config['nRun']
        filename = filename_prefix+f'_{mode}_{freq_start*1e-9:.6f}GHz_span{freq_span*1.e-6:.2f}MHz_rbw{rbw:.0f}Hz_{meas_time:.1f}sec_{nAve:d}counts_{nRun:d}runs'

        if i == 0:
            ms = None
            nosetting = False
        else:
            ms = ret
            nosetting = True
            if mode != mode0:
                nosetting = False
            else:
                if freq_span != freq_span0: ms.freq_span = freq_span
                if rbw != rbw0: ms.band_wid = rbw
                if meas_time != meas_time0: ms.ana_time = meas_time
                if freq_start != freq_start0: ms.freq_start = freq_start
                if nAve != nAve0: ms.trace_nAve = nAve
                #ms.print_fft_setting()
                pass
            pass
        mode0 = mode
        freq_start0 = freq_start
        freq_span0 = freq_span
        rbw0 = rbw
        meas_time0 = meas_time
        nAve0 = nAve
        nRun0 = nRun

        try:
            ret = MS2840A.main(
                ms         = ms,
                mode       = mode,
                freq_start = freq_start,
                freq_span  = freq_span,
                rbw        = rbw,
                meas_time  = meas_time,
                nAve       = nAve,
                nRun       = nRun,
                outdir     = outdir,
                filename   = filename,
                nosetting  = nosetting,
                noplot     = noplot,
                overwrite  = overwrite,
                shortconfig= shortconfig,
                nosubdir   = nosubdir,
                noRun      = noRun,
                filename_add_suffix = filename_add_suffix,
                datBinary=True, saveDat=True, savePickle=True,
                verbose    = 1)
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

    mode = 'SEARCH'
    freq_start = 7.94875 # GHz
    outdir = 'aho'
    nRun_search = 30 # 1 min ごと、これを60回 shellscipt の方でまわす
    scan_span = 2.5e+6 # Hz
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', dest='mode', type=str, default=mode, help=f'SEARCH or Yfactor (default: {mode})')
    parser.add_argument('-s', '--fstart', dest='freq_start', type=float, default=freq_start, help=f'Start Frequency [GHz] (default: {freq_start})')
    parser.add_argument('-o', '--outdir', default=outdir, help=f'Output directory name (default: {outdir})')
    parser.add_argument('--noRun', dest='noRun', action='store_true', default=False, help=f'Only show configurations (Not run measurements)')
    # options for additional measurements
    parser.add_argument('--nRun-search', dest='nRun_search', type=int, default=nRun_search, help=f'# of runs for each band in search (default: {nRun_search})')
    parser.add_argument('--scan-span', dest='scan_span', type=float, default=scan_span, help=f'Frequency span in one scan [Hz] (default: {scan_span})')
    args = parser.parse_args()

    if args.noRun:
        run = False
        pass

    if args.mode == 'SEARCH':
        nRuns = [args.nRun_search] # times
        meas_times = [2] # sec
    elif args.mode == 'YFACTOR':
        nRuns = [5] # times
        meas_times = [2] # sec 2秒を5セット、10秒間取る
    else:

        sys.exit(1)
        pass

    freq_start = args.freq_start
    outdir = args.outdir

    # Scan parameters
    modes = ['FFT'] # FFT or SWEEP
    nAves = [1] # times
    freq_spans  = [int(1e3)] # Hz
    rbws = [10] # Hz
    startHz = int(freq_start*1e+9) # GHz --> Hz
    spanHz = int(args.scan_span) # 2.5 MHz
    # edgeHz = int(250e+3) # 250kHz
    # dHz = int(2e+6) # 2MHz
    freq_starts = [freq_start*1e+9] # Hz

    # freq_starts: Hz --> GHz
    print(f'freq_stars [Hz]: {freq_starts}')
    configs = np.array(create_configs(modes, freq_starts, freq_spans, rbws, meas_times, nAves, nRuns))

    print(f'configs (size={len(configs)}):')
    print(configs)
    run_scanpars(configs, noplot=noplot, overwrite=overwrite, shortconfig=shortconfig,
            filename_prefix=filename_prefix, outdir=outdir, noRun=(not run))
    pass
