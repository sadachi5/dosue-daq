# DOSUE-Y IF test at 4K
. /home/dosue/venv/env1/bin/activate
suffix=$1

for n in {1..20}; do (

python3 ../APSYN420/APSYN420.py --on -f $((n*1000000000))

sleep 10
echo "sleeping in 10 sec."

python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_APSYNtrial_$((n))GHz$1 -m 'SWEEP' -s $((n*1000000000 - 150 )) -w 300 -r 30 -n 1 --att 0 --nRun 1 --overwrite

sleep 2

);
done

python3 ../APSYN420/APSYN420.py --off

