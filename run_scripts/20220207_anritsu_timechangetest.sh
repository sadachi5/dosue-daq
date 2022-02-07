#!/bin/bash

IP='192.168.215.248'

#### 20 GHz, -20 dBm  signal generator input ###
python3 ../ms2840a/ms2840a.py -i $IP -m 'SWEEP' -s 19.999999 -w 2. -r 0.1 -n 100 --nRun 1 -f SG29GHz_SWEEP_test --overwrite
python3 ../ms2840a/ms2840a.py -i $IP -m 'FFT' -s 19.999999 -w 2. -r 0.1 -n 1 --nRun 1 -f SG29GHz_FFT_test --overwrite


:<<'#__COMMENTOUT__'
for i in `seq 1 150`
do
    time=`date +%s`
    filename="SG20GHz_sweep_timechangecheck_SWEEP_${i}_${time}"
    echo $filename
    python3 ../ms2840a/ms2840a.py -i $IP -m 'SWEEP' -s 19.999999 -w 2. -r 100 -n 100 --nRun 1 -f $filename
    time=`date +%s`
    filename="SG20GHz_sweep_timechangecheck_FFT_${i}_${time}"
    echo $filename
    python3 ../ms2840a/ms2840a.py -i $IP -m 'FFT' -s 19.999999 -w 2. -r 100 -n 1 --nRun 1 -f $filename
    echo 'sleeping 10 min'
    sleep 600
done
#__COMMENTOUT__
