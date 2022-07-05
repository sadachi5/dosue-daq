#!/bin/bash

### FFT mode ###
#python3 MS2840A.py -m 'FFT' -s 19999950e+3 -w 100e+3 -r 1000 -t 1 -n 1 --nRun 1 -f test_FFT1
#python3 MS2840A.py -m 'FFT' -s 20e+9 -w 2500e+3 -r 300 -t 1 -n 10 --nRun 10 -f test_FFT2
#python3 MS2840A.py -m 'FFT' -s 20e+9 -w 2500e+3 -r 300 -t 1 -n 2 --nRun 2 -f test_FFT3
#python3 MS2840A.py -m 'FFT' -s 20e+9 -w 2500e+3 -r 1000 -t 1 -n 10 --nRun 1 -f test_FFT --noplot --overwrite
#python3 MS2840A.py -m 'FFT' -s 20e+9 -w 2500e+3 -r 1000 -t 2 -n 1 --nRun 1 -f test_FFT --noplot --overwrite
#python3 MS2840A.py -m 'FFT' -s 20e+9 -w 2500e+3 -r 300 -t 1 -n 1 --nRun 2 -f test --noplot --overwrite
#python3 MS2840A.py -m 'FFT' -s 20e+9 -w 2500e+3 -r 300 -t 10 -n 1 --nRun 12 -f FFT_2.5MHz_10sec_12times --noplot

#python3 MS2840A.py -m 'FFT' -s 19999900e+3 -w 2500e+3 -r 1000 -t 2 -n 1 --nRun 2 -v 2 -f test_FFT --overwrite | tee test_FFT.out


### SWEEP mode ###

#python3 MS2840A.py -m 'SWEEP' -s 19999950e+3 -w 100e+3 -r 300 -n 1 --nRun 1 -f test_SWEEP
#python3 MS2840A.py -m 'SWEEP' -s 18e+9 -w 8500e+6 -r 1e+6 -n 1 --nRun 1 -f test_SWEEP2
#python3 MS2840A.py -m 'SWEEP' -s 18e+9 -w 8500e+6 -r 1e+6 -n 1 --nRun 1 -f SWEEP_plate_test

#python3 MS2840A.py -m 'SWEEP' -s 18e+9 -w 8500e+6 -r 1e+6 -n 1 --nRun 2 -v 2 -f test_SWEEP --overwrite | tee test_SWEEP.out


#python3 MS2840A.py -m 'FFT' -s 19999900e+3 -w 2500e+3 -r 1000 -t 2 -n 1 --nRun 2 -v 2 -f test_FFT --overwrite 2>&1>& test_FFT.out &
