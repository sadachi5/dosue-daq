#!/bin/bash
# -m: mode, -s: start freq [GHz], -w: span [kHz], -r: rbw [kHz], -t: time [s], -n: avarage time, --nRun: number of save, -f: file name for save
# 2021/10/29
# before scan 10:00
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f plate_fft
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f 300K_fft
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f 77K_fft
# after scan 13:30
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f plate_fft_later
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f 300K_fft_later
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f 77K_fft_later
# one more 17:40
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f 77K_fft_las
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f 300K_fft_las
#python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f plate_fft_las

# 2021/11/16
#python3 ms2840a.py -m 'FFT' -s 19.999995 -w 10 -r 0.3 -t 10 -n 1 --nRun 1 -f test

# 2021/11/16
#python3 ms2840a.py -m 'FFT' -s 19.999995 -w 10 -r 0.3 -t 10 -n 1 --nRun 1 -f test

# 2021/11/25
#python3 ms2840a.py -m 'FFT' -s 19.999995 -w 10 -r 0.3 -t 10e-3 -n 1 --nRun 1 -f test    

# 2021/11/29
#python3 ms2840a.py -m 'FFT' -s 26.3 -w 100.e+3 -r 100.0 -t 10 -n 1 --nRun 1 -f test1
#python3 ms2840a.py -m 'FFT' -s 26.349 -w 2.e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f test2
#python3 ms2840a.py -m 'FFT' -s 26.349 -w 1.e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f test3
#python3 ms2840a.py -m 'FFT' -s 26.349 -w 2.e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f test4
#python3 ms2840a.py -m 'FFT' -s 26.345 -w 10.e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f test5
#python3 ms2840a.py -m 'FFT' -s 26.3495 -w 1.e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f test6
#python3 ms2840a.py -m 'FFT' -s 26.349 -w 2.e+3 -r 1.0 -t 2 -n 1 --nRun 1 -f test7
#python3 ms2840a.py -m 'FFT' -s 26.3495 -w 1.e+3 -r 1.0 -t 2 -n 1 --nRun 1 -f test8
#python3 ms2840a.py -m 'FFT' -s 26.345 -w 10.e+3 -r 1.0 -t 2 -n 1 --nRun 1 -f test9

# This setup is for Y-factor. Run for 50 bands i.e. 100 MHz band and 2 MHz steps 
#python3 ms2840a.py -m 'FFT' -s 26.3 -w 2.5e+3 -r 0.3 -t 2 -n 1 --nRun 1 -f test10
#python3 ms2840a.py -m 'FFT' -s 26.345 -w 10.e+3 -r 1.0 -t 2 -n 1 --nRun 1 -f test11

# 2021/12/16
# diffraction effect measurement
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 10.5e+3 -r 1.0 -t 2 -n 100 --nRun 1 -f test1
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 10.5e+3 -r 1.0 -t 2 -n 100 --nRun 1 -f test2
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.0 -t 2 -n 10 --nRun 1 -f test3
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.0 -t 1 -n 100 --nRun 1 -f on_window_300K
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.0 -t 1 -n 100 --nRun 1 -f on_window_77K 
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.0 -t 1 -n 100 --nRun 1 -f on_antenna_300K
#python3 ms2840a.py -m 'SWEEP' -s 18.0 -w 8.5e+6 -r 1.0 -t 1 -n 100 --nRun 1 -f on_antenna_77K

# 2022/01/06
# Aeff measurement
# filename is argv[2] + "_" + argv[3] + "GHz_" + argv[1] + ".dat"
#python3 ms2840a.py -m 'FFT' -s 19.999995 -w 10 -r 0.3 -t 1 -n 1 --nRun 1 -f test0@Aeff_m40_p40@18

# 2022/01/21
# DP diffraction measurement
python3 ms2840a.py -m 'FFT' -s 19.999995 -w 10 -r 0.3 -t 1 -n 1 --nRun 1 -f test0@Aeff_m40_p40@18
