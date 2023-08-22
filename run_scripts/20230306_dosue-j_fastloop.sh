#!/bin/bash
OPT='--shortconfig --datBinary --noplot --nosubdir'
#OPT='--shortconfig --datBinary --nosubdir'
OUTDIR='/data/ms2840a/2023-03-06_loop4'
nAve=1

#OUTNAME="300K_SWEEP"
#CMD0="python3 ../MS2840A/MS2840A.py -m SWEEP -s 8e+9 -w 10e+9 -r 1e+6 -n 1 --nAve $nAve -o $OUTDIR $OPT"

OUTNAME="300K_FFT"
CMD0="python3 ../MS2840A/MS2840A.py -m FFT -s 10e+9 -w 2.5e+6 -r 300 -n 1 --nAve $nAve -o $OUTDIR $OPT"

# test
CMD="${CMD0} -f ${OUTNAME} --overwrite"

I=0
while :
do
    time=`date +%Y-%m-%d-%H:%M:%S`
    echo "${I} th measurement ${time}"
    CMD="${CMD0} -f ${OUTNAME}_SWEEP_${I}"
    $CMD
    I=`expr $I + 1`
    echo $CMD
    echo "sleep 60 seconds"
    for T in {1..1}; do
        sleep 1
        # 進捗10%あたりドットを２つ ".." を出力
        NDOT=`expr ${T} / 3`
        BAR="$(yes \# | head -n ${NDOT} | tr -d '\n')"
        printf "\r[%3d/60] %s" ${T} ${BAR}
        done
    printf "\n"
done
