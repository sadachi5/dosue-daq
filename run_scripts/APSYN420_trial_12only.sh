# DOSUE-Y IF test at 4K
. /home/dosue/venv/env1/bin/activate
suffix=$1

currentdate=`date +%y%m%d`

outputfile=/home/hanimura/dataA/ms2840a/other_data/APSYN_freq_instability/runtime_12GHz_5.dat


python3 ../APSYN420/APSYN420.py --on -f 12000000000

#start_time=`date +%s`

for n in {1..200}; do (

python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_APSYNtrial_12GHz_$((n))_3 -m 'SWEEP' -s 11999999850 -w 300 -r 30 -n 1 --att 0 --nRun 1 --overwrite

finish_time=`date +%s`

#runtime=$((finish_time - start_time))

echo "$((finish_time))" >> $outputfile

echo "ファイル '$outputfile' にデータを書き込みました。"

#sleep 5

);

done

python3 ../APSYN420/APSYN420.py --off

