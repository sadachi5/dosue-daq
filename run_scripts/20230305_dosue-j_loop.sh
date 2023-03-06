#!/bin/bash
OPT='--shortconfig --datBinary --noplot --nosubdir'
#OPT='--shortconfig --datBinary --nosubdir'
OUTDIR='/data/ms2840a/2023-03-05_loop'
nAve=100

# test
#python3 ../MS2840A/MS2840A.py -m 'SWEEP' -s 8e+9 -w 10e+9 -r 1e+6 -n 1 --nAve $nAve -f 300K_SWEEP -o $OUTDIR $OPT --overwrite

I=0
while :
do
    time=`date +%Y-%m-%d-%H:%M:%S`
    echo "${I} th measurement ${time}"
    CMD="python3 ../MS2840A/MS2840A.py -m SWEEP -s 8e+9 -w 10e+9 -r 1e+6 -n 1 --nAve $nAve -f 300K_SWEEP_${I} -o $OUTDIR $OPT"
    $CMD
    I=`expr $I + 1`
    echo $CMD
    echo "sleep 60 seconds"
    for T in {1..60}; do
        sleep 1
        # 進捗10%あたりドットを２つ ".." を出力
        NDOT=`expr ${T} / 3`
        BAR="$(yes \# | head -n ${NDOT} | tr -d '\n')"
        printf "\r[%3d/60] %s" ${T} ${BAR}
        done
    printf "\n"
done
