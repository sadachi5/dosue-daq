# DOSUE-K test at 300K
IP='192.168.215.217'

filename='test'
#python3 ../N9010A/N9010A.py -i $IP -m 'SWEEP' -s 2 -w 30e+6 -r 300e+3 -n 1 -p 10001 -f $filename --overwrite

#filename='NoAmp'
filename='OnlyWarmAmp3'
#filename='AllAmp'
python3 ../N9010A/N9010A.py -i $IP -m 'SWEEP' -s 2 -w 30e+6 -r 300e+3 -n 1 -p 10001 -f $filename
