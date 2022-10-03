# DOSUE-Y test
suffix=$1

# 77K
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_230GHz_77K-$1 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 10 --att 0 --nRun 1


# 77K
python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_230GHz_WinScan2-$1 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 1 --att 0 --nRun 10
