# DOSUE-Y IF test at 4K
suffix=$1
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_NoAmp_SWEEP -m 'SWEEP' -s 2e+9 -w 18e+9 -r 10e+6 -n 100 --att 0 --nRun 1 --overwrite
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_WarmAmp_SWEEP -m 'SWEEP' -s 2e+9 -w 18e+9 -r 10e+6 -n 100 --att 0 --nRun 1 --overwrite
python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_AllAmp_SWEEP$1 -m 'SWEEP' -s 2e+9 -w 18e+9 -r 10e+6 -n 100 --att 0 --nRun 1 --overwrite

#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_AllAmp_SWEEP_many$1 -m 'SWEEP' -s 4e+9 -w 8e+9 -r 10e+6 -n 1 --att 0 --nRun 100 --overwrite
