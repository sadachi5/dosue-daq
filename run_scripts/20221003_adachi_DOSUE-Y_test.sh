# DOSUE-Y test
suffix=$1

# 77K
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_230GHz_77K-$1 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 10 --att 0 --nRun 1

# window scan
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_230GHz_WinScan2-$1 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 1 --att 0 --nRun 10

# at room temperature / NoSIS
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_NoSIS_CISO50ohm_warm$1 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 10 --att 0 --nRun 1 --overwrite

# test
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test1 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 10 --att 0 --nRun 1 --overwrite
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test2 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 10 --att 0 --nRun 2 --overwrite
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test3 -o /data/ms2840a/test -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 10 --att 0 --nRun 1 --overwrite --nosubdir
#python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test4 -o /data/ms2840a/test -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 10 --att 0 --nRun 2 --overwrite --nosubdir
