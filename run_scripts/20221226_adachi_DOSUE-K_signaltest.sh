# DOSUE-Y test
IP="192.168.215.228"
suffix=$1

# signal test (input: signal generator + x2 freq. multiplier)
#file="test"
pfreq="25"
freq="26"
file="DOSUE-K_${freq}GHz"
python3 ../MS2840A/MS2840A.py -i $IP -f $file -o /data/ms2840a/2022-12-26_signaltest -m 'FFT' -s ${pfreq}984375000 -w 31250000 -r 300 -n 1 --att 0 --nRun 1  --nosubdir
