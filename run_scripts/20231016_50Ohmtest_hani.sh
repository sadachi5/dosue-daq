# DOSUE-Y IF test at 4K
. /home/dosue/venv/env1/bin/activate
suffix=$1

python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_$1 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 200 --att 0 --nRun 1 --overwrite
