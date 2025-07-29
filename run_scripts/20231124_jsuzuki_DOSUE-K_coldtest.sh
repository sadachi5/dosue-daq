# DOSUE-K test at 3K
IP='192.168.215.80'

BASE_PATH=/home/dosue/dosue-daq
#filename='test'
#python3 ../N9010A/N9010A.py -i $IP -m 'SWEEP' -s 2 -w 30e+6 -r 300e+3 -n 1 -p 10001 -f $filename --overwrite

#filename='NoAmp'
#filename='OnlyWarmAmp'
#filename='AllAmp2'
#python3 ../N9010A/N9010A.py -i $IP -m 'SWEEP' -s 2 -w 30e+6 -r 300e+3 -n 1 -p 10001 -f $filename


#filename='Yfactor300K3'
#filename='Yfactor77K'
filename='YfactorMagnet'
python3 ${BASE_PATH}/N9010A/N9010A.py -i $IP -m 'SWEEP' -s 2 -w 30e+6 -r 300e+3 -n 1 -p 10001 -f $filename

#filename='test2'
#python3 ../N9010A/N9010A.py -i $IP -m 'SWEEP' -s 18 -w 1e+4 -r 300 -n 1 -p 40001 -f $filename
