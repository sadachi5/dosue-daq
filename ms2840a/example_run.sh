#!/bin/bash

# FFT mode
#python3 ms2840a.py -m 'FFT' -s 19.99995 -w 1.0e+2 -r 1.0 -t 1 -n 1 --nRun 1 -f test_FFT1
#python3 ms2840a.py -m 'FFT' -s 20.0 -w 2.5e+3 -r 0.3 -t 1 -n 10 --nRun 10 -f test_FFT2
python3 ms2840a.py -m 'FFT' -s 20.0 -w 2.5e+3 -r 0.3 -t 1 -n 2 --nRun 2 -f test_FFT3

# SWEEP mode
#python3 ms2840a.py -m 'SWEEP' -s 19.99995 -w 1.0e+2 -r 0.3 -n 1 --nRun 1 -f test_SWEEP1
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.e+3 -n 1 --nRun 1 -f test_SWEEP2
