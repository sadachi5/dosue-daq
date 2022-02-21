#!/bin/bash

for i in {18..26}; do
    python3 xy_scan.py -o /data/xy_scan/2022-02-21/x_center_test_${i}GHz -f ${i} -v 1
done
