#!/bin/env python3
import os
import sys
import numpy as np

def check_exist_data(freq_start_GHz, path):

    startHz = int(freq_start_GHz*1e+9) # GHz --> Hz
    spanHz = int(100*1e+6) # 100MHz
    edgeHz = int(250e+3) # 250kHz
    dHz = int(2e+6) # 2MHz
    check_freq_starts = np.arange( startHz - edgeHz, startHz + spanHz - edgeHz, dHz ) # Hz

    existfiles = np.sort(os.listdir(path))
    overlapped = False
    for ef in existfiles:
        try:
            _start_GHz = float(ef.split('_')[2][:-3]) # scan_FFT_10.075750GHz_span2.50MHz_rbw300Hz_2.0sec_1counts_1runs.csv
            _start_Hz = int(_start_GHz * 1e+9)
        except Exception:
            #print(f'{ef} is not expected file name to check frequency. -> skip checking')
            continue
        if _start_Hz in check_freq_starts:
            print(f'There is overlapped frequency! freq_start = {_start_GHz:.6f} GHz / check_freq_start = {freq_start_GHz} GHz')
            overlapped = True
            print(ef)
            pass
        pass
    return overlapped


if __name__ == '__main__':
    freq_start = float(sys.argv[1]) # GHz
    path = sys.argv[2]
    check_exist_data(freq_start, path)
