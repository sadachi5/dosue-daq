#!/bin/bash

IP='192.168.215.88'

#### 20 GHz, -20 dBm  signal generator input ###
#python3 ../n9010a/n9010a.py -i $IP -s 19.999999 -w 2. -r 0.091 -n 100 -p 1001 -f SG20GHz_test --overwrite


#:<<'#__COMMENTOUT__'
for i in `seq 1 150`
do
    time=`date +%s`
    filename="SG20GHz_sweep_timechangecheck_${i}_${time}"
    echo $filename
    python3 ../n9010a/n9010a.py -i $IP -s 19.999999 -w 2. -r 0.091 -n 100 -p 1001 -f $filename
    echo 'sleeping 10 min'
    sleep 600
done
#__COMMENTOUT__
