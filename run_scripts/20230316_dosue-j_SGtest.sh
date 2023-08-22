# -10dBm + junkosha-long-SMA-cable + -20 dBm Att. + pasternack antenna

# Open the front panel
# Antenna located in the front
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f SG10GHz_-10dBm
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 14.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f SG15GHz_-10dBm
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f test10GHz
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 -t 0.1 --nRun 1 -f test10GHz_time0.1
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 -t 0.01 --nRun 1 -f test10GHz_time0.01
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 -t 0.008 --nRun 1 -f test10GHz_time0.008
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 -t 0.001 --nRun 1 -f test10GHz_time0.001
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 -t 0.0001 --nRun 1 -f test10GHz_time0.0001
python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 -t 0.00001 --nRun 1 -f test10GHz_time0.00001

# Close the front panel
# Antenna located in the front
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f SG10GHz_-10dBm_DarkBox1
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 14.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f SG15GHz_-10dBm_DarkBox1
# Antenna located on the bottom
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f SG10GHz_-10dBm_DarkBox2
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 14.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f SG15GHz_-10dBm_DarkBox2
# Antenna located on 45deg side
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 9.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f SG10GHz_-10dBm_DarkBox3
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 14.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 1 -f SG15GHz_-10dBm_DarkBox3_2
