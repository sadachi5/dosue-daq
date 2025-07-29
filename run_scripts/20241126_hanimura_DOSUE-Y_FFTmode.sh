# DOSUE-Y FFT mode
. /home/dosue/venv/env1/bin/activate
suffix=$1

python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_FFT_$1 -m 'FFT' -s 7.94875e+9 -w 2.5e6 -r 300 -t 50 --att 0 --nRun 1 --nAve 1 --overwrite
