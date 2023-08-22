# SWEEP: 5GHz wifi check
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 0.0e+9 -w 20e+9 -r 1e+6 -n 1 --nRun 1 -f wifi0-20GHz_RBW1MHz_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 9.0e+9 -w 1e+9 -r 1e+6 -n 1 --nRun 10 -f wifi9-10GHz_RBW10MHz_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 2.0e+9 -w 10e+9 -r 1e+6 -n 1 --nRun 10 -f wifi2-12GHz_RBW10MHz_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 10.0e+9 -w 2e+9 -r 1e+6 -t 2 -n 1 --nRun 30 -f wifi10-12GHz_RBW10MHz_time2_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 4.0e+9 -w 10e+9 -r 1e+6 -t 10 -n 1 --nRun 10 -f wifi4-14GHz_RBW10MHz_time10_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.0e+9 -w 1e+9 -r 10e+3 -n 1 --nRun 10 -f wifi5-6GHzSWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.4e+9 -w 2e+8 -r 3e+3 -n 1 --nRun 1 -f wifi5.4-5.6GHzSWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.48e+9 -w 4e+7 -r 3e+3 -n 1 --nRun 10 -f wifi_5.48-5.52GHz_RWB3kHz_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.48e+9 -w 4e+7 -r 10e+3 -n 1 --nRun 10 -f wifi_5.48-5.52GHz_RWB10kHz_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1 --nRun 10 -f wifi_5.49-5.50GHz_RBW10kHz_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1 -t 0.1 --nRun 10 -f wifi_5.49-5.50GHz_RBW10kHz_time0.1_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1 -t 1 --nRun 10 -f wifi_5.49-5.50GHz_RBW10kHz_time1_SWEEP --overwrite # --> peak 見える
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1 -t 10 --nRun 10 -f wifi_5.49-5.50GHz_RBW10kHz_time10_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.49e+9 -w 10e+6 -r 3e+3 -n 1 --nRun 10 -f wifi_5.49-5.50GHz_RBW3kHz_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r   1e+3 -n 1 -t 1 --nRun 10 -f wifi_5.45-5.55GHz_RBW1kHz_time1_SWEEP --overwrite # --> small peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r   3e+3 -n 1 -t 1 --nRun 10 -f wifi_5.45-5.55GHz_RBW3kHz_time1_SWEEP --overwrite # -->  small peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r  10e+3 -n 1 -t 1 --nRun 10 -f wifi_5.45-5.55GHz_RBW10kHz_time1_SWEEP --overwrite # -->  small peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r  30e+3 -n 1 -t 1 --nRun 10 -f wifi_5.45-5.55GHz_RBW30kHz_time1_SWEEP --overwrite # -->  small peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 100e+3 -n 1 -t 1 --nRun 10 -f wifi_5.45-5.55GHz_RBW100kHz_time1_SWEEP --overwrite # -->  small peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 300e+3 -n 1 -t 1 --nRun 10 -f wifi_5.45-5.55GHz_RBW300kHz_time1_SWEEP --overwrite # --> large peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r   1e+6 -n 1 -t 1 --nRun 10 -f wifi_5.45-5.55GHz_RBW1MHz_time1_SWEEP --overwrite # --> large peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 100e+3 -n 1 -t   10 --nRun 10 -f wifi_5.45-5.55GHz_RBW100kHz_time10_SWEEP --overwrite # --> 
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 300e+3 -n 1 -t    3 --nRun 10 -f wifi_5.45-5.55GHz_RBW300kHz_time3_SWEEP --overwrite # --> 
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 3e+6 -n 1 -t 0.1 --nRun 10 -f wifi_5.45-5.55GHz_RBW3MHz_time0.1_SWEEP --overwrite # --> large peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 3e+6 -n 1 -t 0.1 --nRun 100 -f wifi_5.45-5.55GHz_RBW3MHz_time0.1_nRun100_SWEEP --overwrite # --> large peak
# Best peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 1e+6 -n 1 -t 0.1 --nRun 100 -f wifi_5.45-5.55GHz_RBW1MHz_time0.1_nRun100_SWEEP_3 --overwrite # --> large peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 1e+6 -n 1 -t 0.05 --nRun 100 -f wifi_5.45-5.55GHz_RBW1MHz_time0.05_nRun100_SWEEP_2 --overwrite # --> large peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 1e+6 -n 1 -t 0.01 --nRun 100 -f wifi_5.45-5.55GHz_RBW1MHz_time0.01_nRun100_SWEEP_2 --overwrite # --> time was set to 0.001 / No peak
# Best peak config without amp
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 1e+6 -n 1 -t 0.1 --nRun 100 -f wifiNoAmp_5.45-5.55GHz_RBW1MHz_time0.1_nRun100_SWEEP_2 --overwrite # -->
# Best peak config with BB cover (amp=ON, blackbody on the antenna aperture)
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 1e+6 -n 1 -t 0.1 --nRun 100 -f wifiBBcover_5.45-5.55GHz_RBW1MHz_time0.1_nRun100_SWEEP_2 --overwrite # -->

# FFT: 5GHz wifi check
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 4.9995e+9 -w 1e+6 -r 300 -n 1 --nRun 10 -t 1 -f wifi5GHz --overwrite
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.1995e+9 -w 1e+6 -r 300 -n 1 --nRun 10 -t 1 -f wifi5.2GHz --overwrite
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.2995e+9 -w 1e+6 -r 300 -n 1 --nRun 10 -t 1 -f wifi5.3GHz --overwrite
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.5995e+9 -w 1e+6 -r 300 -n 1 --nRun 10 -t 1 -f wifi5.6GHz --overwrite
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.4995e+9 -w 1e+6 -r 300 -n 1 --nRun 10 -t 1 -f wifi5.5GHz --overwrite

# FFT: 5GHz wifi check
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 100 --nRun 1 -t 1 -f wifi_5.49GHz_RBW10kHz_nAve100_FFT --overwrite
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1 --nRun 10 -f wifi_5.49GHz_RBW10kHz_autotime_FFT --overwrite
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.491e+9 -w 2e+6 -r 300 -n 1 --nRun 10 -t 2 -f wifi_5.49GHz_span2MHz_RBW300Hz_time2_FFT --overwrite # --> X
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.491e+9 -w 2e+6 -r 300 -n 1 --nRun 10 -t 0.01 -f wifi_5.49GHz_span2MHz_RBW300Hz_time0.01_FFT --overwrite # --> X
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.491e+9 -w 10e+6 -r 300 -n 1 --nRun 1 -t 0.01 -f wifi_5.49GHz_span10MHz_RBW300Hz_time0.01_FFT --overwrite # --> X
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1   --nRun 10 -t 0.1  -f wifi_5.49GHz_RBW10kHz_time0.1_FFT --overwrite # --> peak が見える
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 100 --nRun 1  -t 0.1  -f wifi_5.49GHz_RBW10kHz_time0.1_nAve100_FFT --overwrite
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1   --nRun 10 -t 0.01 -f wifi_5.49GHz_RBW10kHz_time0.01_FFT --overwrite # --> peak 時々見える
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1   --nRun 100 -t 0.01 -f wifi_5.49GHz_RBW10kHz_time0.01_nRun100_FFT --overwrite # --> peak 時々見える
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 100  --nRun 1 -t 0.01 -f wifi_5.49GHz_RBW10kHz_time0.01_nAve100_FFT --overwrite
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1   --nRun 10 -t 0.001 -f wifi_5.49GHz_RBW10kHz_time0.001_FFT --overwrite # --> peak 稀に見える
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 1 --nRun 100 -t 0.001 -f wifi_5.49GHz_RBW10kHz_time0.001_nRun100_FFT_2 --overwrite # --> peak 稀に見える
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 10e+6 -r 3e+3 -n 1 --nRun 1 -t 1 -f wifi_5.49GHz_RBW3kHz_FFT --overwrite

# FFT: 5GHz averaging
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 5.49e+9 -w 32e+6 -r 1e+6 -n 100 --nRun 1  -t 0.01  -f wifi_5.49GHz_RBW1MHz_time0.1_nAve100_FFT --overwrite # --> X
# SWEEP: 5GHz averaging
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.49e+9 -w 10e+6 -r 10e+3 -n 100 -t 1 --nRun 1 -f wifi_5.49-5.50GHz_RBW10kHz_time1_nAve100_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.49e+9 -w 10e+6 -r 1e+6 -n 100 -t 1 --nRun 1 -f wifi_5.49-5.50GHz_RBW1MHz_time1_nAve100_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 0.3e+6 -n 10 -t 1 --nRun 1 -f wifi_5.45-5.55GHz_RBW0.3MHz_time1_nAve10_SWEEP --overwrite # --> large peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 0.3e+6 -n 100 -t 1 --nRun 1 -f wifi_5.45-5.55GHz_RBW0.3MHz_time1_nAve100_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 1e+6 -n 10 -t 1 --nRun 1 -f wifi_5.45-5.55GHz_RBW1MHz_time1_nAve10_SWEEP --overwrite # --> large peak
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 5.45e+9 -w 100e+6 -r 1e+6 -n 100 -t 1 --nRun 1 -f wifi_5.45-5.55GHz_RBW1MHz_time1_nAve100_SWEEP --overwrite

# SWEEP: 10GHz wifi check
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 10.98e+9 -w 20e+6 -r 10e+3 -n 1 -t 2 --nRun 10 -f wifi_10.98-11.00GHz_RBW10kHz_time2_SWEEP --overwrite # --> X
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 10.9e+9 -w 200e+6 -r 1e+6 -n 1 -t 0.2 --nRun 100 -f wifi_10.9-11.1GHz_RBW1MHz_time0.2_nRun100_SWEEP_2 --overwrite #  --> X
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 10.9e+9 -w 200e+6 -r 1e+6 -n 1 --nRun 100 -f wifi_10.9-11.1GHz_RBW1MHz_nRun100_SWEEP --overwrite #  --> X

# FFT: 10GHz wifi check
#python3 ../MS2840A/MS2840A.py -m 'FFT' -s 10.98e+9 -w 10e+6 -r 10e+3 -n 1 --nRun 100 -t 0.001 -f wifi_10.98GHz_RBW10kHz_time0.001_nRun100_FFT_2 --overwrite # --> X

# SWEEP: 10GHz averaging
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 10.9e+9 -w 200e+6 -r 0.3e+6 -n 10 -t 2 --nRun 1 -f wifi_10.9-11.1GHz_RBW0.3MHz_time2_nAve10_SWEEP --overwrite # --> X
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 10.9e+9 -w 200e+6 -r 1e+6 -n 10 -t 2 --nRun 1 -f wifi_10.9-11.1GHz_RBW1MHz_time2_nAve10_SWEEP --overwrite # --> X


# SWEEP: 8--14 GHz spurious peaks (open front panel)
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 8.0e+9 -w 6e+9 -r 1e+6 -n 1 --nRun 10 -t 1 -f spurious8-14GHz_RBW1MHz_SWEEP --overwrite
# SWEEP: 8--18 GHz spurious peaks (open front panel)
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 8.0e+9 -w 10e+9 -r 1e+6 -n 1 --nRun 100 -f spurious8-14GHz_RBW1MHz_autotime_nRun100_SWEEP --overwrite
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 8.0e+9 -w 10e+9 -r 1e+6 -n 100 --nRun 1 -f spurious8-14GHz_RBW1MHz_autotime_nAve100_SWEEP --overwrite
python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 8.0e+9 -w 10e+9 -r 1e+6 -n 100 --nRun 1 -t 1 -f spurious8-14GHz_RBW1MHz_time1_nAve100_SWEEP --overwrite
