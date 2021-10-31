#!/bin/bash

### FFT mode ###
#python3 ms2840a.py -m 'FFT' -s 19.99995 -w 1.0e+2 -r 1.0 -t 1 -n 1 --nRun 1 -f test_FFT1
#python3 ms2840a.py -m 'FFT' -s 20.0 -w 2.5e+3 -r 0.3 -t 1 -n 10 --nRun 10 -f test_FFT2
#python3 ms2840a.py -m 'FFT' -s 20.0 -w 2.5e+3 -r 0.3 -t 1 -n 2 --nRun 2 -f test_FFT3
#python3 ms2840a.py -m 'FFT' -s 20.0 -w 2.5e+3 -r 1 -t 1 -n 10 --nRun 1 -f test_FFT --noplot --overwrite
#python3 ms2840a.py -m 'FFT' -s 20.0 -w 2.5e+3 -r 1 -t 2 -n 1 --nRun 1 -f test_FFT --noplot --overwrite
#python3 ms2840a.py -m 'FFT' -s 20.0 -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 2 -f test --noplot --overwrite
#python3 ms2840a.py -m 'FFT' -s 20.0 -w 2.5e+3 -r 0.3 -t 10 -n 1 --nRun 12 -f FFT_2.5MHz_10sec_12times --noplot

python3 ms2840a.py -m 'FFT' -s 19.9999 -w 2.5e+3 -r 1 -t 2 -n 1 --nRun 2 -v 2 -f test_FFT --overwrite | tee test_FFT.out


### SWEEP mode ###

#python3 ms2840a.py -m 'SWEEP' -s 19.99995 -w 1.0e+2 -r 0.3 -n 1 --nRun 1 -f test_SWEEP
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.e+3 -n 1 --nRun 1 -f test_SWEEP2
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.e+3 -n 1 --nRun 1 -f SWEEP_plate_test

#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.e+3 -n 1 --nRun 2 -v 2 -f test_SWEEP --overwrite | tee test_SWEEP.out
