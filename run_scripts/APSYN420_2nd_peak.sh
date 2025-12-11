# DOSUE-Y IF test at 4K
. /home/dosue/venv/env1/bin/activate
suffix=$1

# 13, 13.5, 14 GHz

python3 ../APSYN420/APSYN420.py --on -f $((135*100000000))

sleep 2
echo "sleeping in 2 sec."

python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_APSYN420_2ndPeak_13.5GHz_w20GHz_RBW100kHz -m 'SWEEP' -s 1000000000 -w 20000000000 -r 100000 -n 1 --att 0 --nRun 1 --overwrite

sleep 2





python3 ../APSYN420/APSYN420.py --off
