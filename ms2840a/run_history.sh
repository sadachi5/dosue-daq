#!/bin/bash
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
python3 ms2840a.py -m 'FFT' -s 26.399975 -w 2.5e+3 -r 1.0 -t 10 -n 1 --nRun 1 -f plate_fft_las
