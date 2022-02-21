#!/bin/bash

OLD_IP='192.168.215.247'
NEW_IP='192.168.215.248'

#### 20 GHz, -20 dBm  signal generator input ###

### OLD MS2840A ###
# FFT mode
#python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'FFT' -s 19.999995 -w 10. -r 0.3 -t 1 -n 1 --nRun 1 -f SG20GHz_fft_TohokuMS2840A_1 --overwrite
#python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'FFT' -s 19.999995 -w 10. -r 0.3 -t 1 -n 1 --nRun 1 -f SG20GHz_fft_TohokuMS2840A_2 --overwrite
# SWEEP mode
#python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'SWEEP' -s 19.999995 -w 10. -r 0.3 -n 1 --nRun 1 -f SG20GHz_sweep_TohokuMS2840A_1 --overwrite
#python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'SWEEP' -s 19.999995 -w 10. -r 0.3 -n 1 --nRun 1 -f SG20GHz_sweep_TohokuMS2840A_2 --overwrite

### NEW MS2840A ###
# FFT mode
#python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 19.999995 -w 10. -r 0.3 -t 1 -n 1 --nRun 1 -f SG20GHz_fft_KyotoMS2840A_1 --overwrite
#python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 19.999995 -w 10. -r 0.3 -t 1 -n 1 --nRun 1 -f SG20GHz_fft_KyotoMS2840A_2 --overwrite
# SWEEP mode
#python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 19.999995 -w 10. -r 0.3 -n 1 --nRun 1 -f SG20GHz_sweep_KyotoMS2840A_1 --overwrite
#python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 19.999995 -w 10. -r 0.3 -n 1 --nRun 1 -f SG20GHz_sweep_KyotoMS2840A_2 --overwrite



#### Y-factor input (warm) ###

### NEW MS2840A ###
# 300K
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft18GHz_KyotoMS2840A_1 --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft20GHz_KyotoMS2840A_1 --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft26GHz_KyotoMS2840A_1 --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_KyotoMS2840A_1 --overwrite
#__COMMENTOUT__
# 77K
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft18GHz_KyotoMS2840A_1 --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft20GHz_KyotoMS2840A_1 --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft26GHz_KyotoMS2840A_1 --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor77K_sweep_KyotoMS2840A_1 --overwrite
#__COMMENTOUT__



### OLD MS2840A ###
# 300K
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft18GHz_TohokuMS2840A_1
python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft20GHz_TohokuMS2840A_1
python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft26GHz_TohokuMS2840A_1
python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_TohokuMS2840A_1
#__COMMENTOUT__
# 77K
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft18GHz_TohokuMS2840A_1
python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft20GHz_TohokuMS2840A_1
python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft26GHz_TohokuMS2840A_1
python3 ../MS2840A/MS2840A.py -i $OLD_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor77K_sweep_TohokuMS2840A_1
#__COMMENTOUT__


### NEW MS2840A ###
# 300K
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft18GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft20GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft26GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_KyotoMS2840A_2
#__COMMENTOUT__
# 77K
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft18GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft20GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft26GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor77K_sweep_KyotoMS2840A_2
#__COMMENTOUT__
# No Amp
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft18GHz_KyotoMS2840A_NoAmp --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft20GHz_KyotoMS2840A_NoAmp --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft26GHz_KyotoMS2840A_NoAmp --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_KyotoMS2840A_NoAmp --overwrite
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 10.e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_KyotoMS2840A_NoAmpRBW10MHz
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 100.e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_KyotoMS2840A_NoAmpRBW100MHz # --> ERROR: out of range of RBW
#__COMMENTOUT__
# 300K
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_KyotoMS2840A_3
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 10.e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_KyotoMS2840A_3_RBW10MHz




### NEW MS2840A ###
I=3 # without bending cable
# 300K
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft18GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft20GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor300K_fft26GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor300K_sweep_KyotoMS2840A_2
#__COMMENTOUT__
# 77K
<<'#__COMMENTOUT__'
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 18. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft18GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 20. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft20GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'FFT' -s 26. -w 2.5e+3 -r 0.3 -t 1 -n 1 --nRun 1 -f Yfactor77K_fft26GHz_KyotoMS2840A_2
python3 ../MS2840A/MS2840A.py -i $NEW_IP -m 'SWEEP' -s 16. -w 10.5e+6 -r 1.0e+3 -n 100 --nRun 1 -f Yfactor77K_sweep_KyotoMS2840A_2
#__COMMENTOUT__


