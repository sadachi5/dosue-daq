#!/bin/bash

SPA_IP='10.10.10.11'

#### ~26.5 GHz, RBW=1MHz,  
python3 ../N9010A/N9010A.py -m SWEEP -i $SPA_IP -s 10e+6 -w 26490e+6 -r 1e+6 -n 1 -p 26491 -f 26_5GHz_test_nAve1 -o /DATA/dosue/Q-band/beam_pattern/20251211/
