# DOSUE-Y SIS test at 4K
suffix=$1
LO=210

#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_SIStest_LO${LO}_SWEEP$1 -m 'SWEEP' -s 2e+9 -w 18e+9 -r 10e+6 -n 100 --att 0 --nRun 1
python3 ../MS2840A/MS2840A.py -f DOSUE-Y_SIStest_LO${LO}_SWEEP2$1 -m 'SWEEP' -s 4e+9 -w 8e+9 -r 10e+6 -n 10 --att 0 --nRun 5 --overwrite
