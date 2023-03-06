#!/bin/bash
mode='300K'
suffix=""
OPT="--shortconfig --overwrite"

if [ $# -gt 0 ]; then
    mode=$1
fi
if [ $# -gt 1 ]; then
    suffix=$2
fi
echo "mode = $mode"
echo "suffix = $suffix"
echo "Is it OK?"
read enter

# freq range: 0--20 GHz with RBW=2MHz (This is minimum RBW because max npoints is 10001.)
if [ "$mode" = "300K" ]; then
    # 300K
    python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 0 -w 20e+9 -r 2e+6 -n 1 --nAve 100 -f 300K_SWEEP${suffix} $OPT
elif [ "$mode" = "77K" ]; then
    # 77K
    python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 0 -w 20e+9 -r 2e+6 -n 1 --nAve 100 -f 77K_SWEEP${suffix} $OPT
fi
