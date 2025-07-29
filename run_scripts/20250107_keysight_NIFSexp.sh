#!/bin/bash

IP='192.168.11.6'

#### ~32 GHz, RBW=1MHz,  
python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 1 -p 31991 -f 32GHz_test_nAve1 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250107_NIFStest --overwrite
python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f 32GHz_test_nAve10 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250107_NIFStest --overwrite
python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 100 -p 31991 -f 32GHz_test_nAve100 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250107_NIFStest --overwrite
