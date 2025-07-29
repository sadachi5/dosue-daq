# DOSUE-Y IF test at 4K
#!bin/bash
. /home/hanimura/virtual/bin/activate

start="7.94875e+9"
width="2.5e6"
rbw="300"
time=2
nRun=1
nAve=1

# meastime=7200
# interval=300
waiting=240
# Ymeasuing=60
repeating_time=24

# # For test
# OPT=''
# #OPT=' --noRun'
# RUN=true
#RUN=false
DIR=2024-11-29
#DIR=test

# source /home/dosue/venv/env1/bin/activate # for python3
LOG1="/data/ms2840a/$DIR/data/timestamp__.dat"
LOG2="/data/ms2840a/$DIR/data/roomtemp__.dat"
LOG3="/data/ms2840a/$DIR/data/V_value__.dat"
LOG4="/data/ms2840a/$DIR/data/I_value__.dat"
# SEARCH="/data/ms2840a/dosue-j/signal_data/$DIR"
# YFACTOR_300K_BEFORE="/data/ms2840a/dosue-j/yfactor_300K_ini/$DIR" # 300K before measurement
# YFACTOR_77K_BEFORE="/data/ms2840a/dosue-j/yfactor_77K_ini/$DIR" # 77K before measurement
# YFACTOR_300K_AFTER="/data/ms2840a/dosue-j/yfactor_300K_fin/$DIR" # 300K after measurement
# YFACTOR_77K_AFTER="/data/ms2840a/dosue-j/yfactor_77K_fin/$DIR" # 77K after measurement


for ((i=1; i<$((repeating_time+1)); i++)); do

    # 1. Y-factor 300K before
    # Measurements (Y-factor & Search & Y-factor)
    starttime=`date +%Y-%m-%d-%H:%M:%S`
    echo -n "$starttime " >> $LOG1
    check_exit_data $YFACTOR_300K_BEFORE
    echo
    echo '########## Y-factor 300K ${i} ##########'

    echo 'How much is the Voltage [mV] of SIS bias? (before 300K measurement)'
    read Vval
    echo -n "$Vval " >> $LOG3

    echo 'How much is the Current [µA] of SIS bias? (before 300K measurement)'
    read Ival
    echo -n "$Ival " >> $LOG4

    echo 'How much is the temperature of the 300K eccosorb? (before 300K measurement)'
    read temp
    echo -n "$temp " >> $LOG2

    echo 'PLL OK? [y/n]'
    read YN

    echo 'Please enter if you prepare for the 300K measurement.'
    read enter
    echo 'Start 300K measurement'

    sleep 1

    python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_FFT_300K_GainFluc_${i+20} -m 'FFT' -s $start -w $width -r $rbw -t $time --att 0 --nRun $nRun --nAve $nAve --overwrite

    echo '########## End of Y-factor 300K before ##########'
    echo

    # 2. Y-factor 77K before
    echo
    echo '########## Y-factor 77K before ##########'
    echo 'Please enter if you prepare for the LN2.'
    read enter
    echo 'Start 77K measurement'

    sleep 1

    python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_FFT_77K_GainFluc_${i} -m 'FFT' -s $start -w $width -r $rbw -t $time --att 0 --nRun $nRun --nAve $nAve --overwrite

    echo '########## End of Y-factor 77K before ##########'

    echo "wait for 4 min..."

    # プログレスバー全体の幅
    box_width=20

    for ((j=1; j<$((waiting+1)); j++)); do

    # 処理を実行
    sleep 1

    # 現在のバーの横幅
    bar_width=$(( box_width * j / waiting ))

    # バーの空きスペース
    space=$(( box_width - bar_width))

    # 現在の割合
    percent=$(( j * 100 / waiting ))

    # バーを出力
    printf '\r['
    yes "#" | head -n "${bar_width}" | tr -d "\n"
    yes " " | head -n "${space}" | tr -d "\n"
    printf "] %s%%" "${percent}"
    done

    ./beep.sh



done

echo ""
echo "END!"
echo ""
