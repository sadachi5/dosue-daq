# DOSUE-Y IF test at 4K
. /home/dosue/venv/env1/bin/activate
suffix=$1
suffix_=$2


python3 ../APSYN420/APSYN420.py --on -f $(($1*1000000000))

python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_LOAPSYN_$2 -m 'SWEEP' -s 3e+9 -w 10e+9 -r 10e+6 -n 100 --att 0 --nRun 1 --overwrite

python3 ../APSYN420/APSYN420.py --off

