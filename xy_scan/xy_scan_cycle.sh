#!/bin/bash

for i in {18..26}; do
    for j in {0..2}; do
        python3 xy_scan.py -o /data/xy_scan/2022-03-08_cycle/${i}GHz_${j}_X -f ${i} -v 1
    done
done

for i in {18..26}; do
    for j in {0..2}; do
        python3 xy_scan.py -o /data/xy_scan/2022-03-08_cycle/${i}GHz_${j}_Y -f ${i} -v 1
    done
done
