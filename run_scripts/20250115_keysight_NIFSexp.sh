#!/bin/bash

IP='192.168.11.8' # SpeAna

#### ~32 GHz, RBW=1MHz,  
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f nothing_test_nAve10 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/2025014-16_NIFSexp --overwrite
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f WAMPON_nAve10 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/2025014-16_NIFSexp --overwrite

# 1MHz
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f WAMPON_nAve10 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite


# Cooling 1

# 10MHz
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 10e+6 -n 10 -p 3200 -f WAMPON_nAve10BW10MHz_cooling -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 10e+6 -n 10 -p 3200 -f Hline_300K_nAve10BW10MHz_cooling -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 10e+6 -n 10 -p 3200 -f Hline_77K_nAve10BW10MHz_cooling -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite


#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 1 -p 31991 -f test_nAve1 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite

# Cooling 2

# 1 MHz
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f Hline_77K_nAve10BW1MHz_cooling2 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f Hline_300K_nAve10BW1MHz_cooling2 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite

# 10 Mhz
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 10e+6 -n 10 -p 3200 -f Hline_300K_nAve10BW10MHz_cooling2 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 10e+6 -n 10 -p 3200 -f Hline_77K_nAve10BW10MHz_cooling2 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite

# test
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 1 -p 31991 -f test_nAve1 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite

# 10 MHz
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f Hline_77K_nAve10BW1MHz_cooling2-2 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f Hline_300K_nAve10BW1MHz_cooling2-2 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite


# 4K

# 1 MHz
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f Hline_300K_nAve10BW1MHz_4K -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n 10 -p 31991 -f Hline_77K_nAve10BW1MHz_4K -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/

# test
#nAve=10
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n ${nAve} -p 31991 -f test_nAve${nAve} -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite

# 4K 2回目
# 1 MHz
nAve=100
#python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n ${nAve} -p 31991 -f Hline_300K_nAve${nAve}BW1MHz_4K-2 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/ --overwrite
python3 ../N9010a/N9010a.py -m SWEEP -i $IP -s 10e+6 -w 31990e+6 -r 1e+6 -n ${nAve} -p 31991 -f Hline_77K_nAve${nAve}BW1MHz_4K-2 -o /Users/adachi/sadachi5/DOSUE/Data/DOSUE-NIFS/20250114-16_NIFSexp/input/
