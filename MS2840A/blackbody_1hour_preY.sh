# 説明
# スペアナを ref してるかしてないかで違いがあるかを調べる
# 7.95 GHz 近傍 (2.5 MHz 帯域) を測定
# 1時間
# 2025/10/02 作成 by hanimura

#!bin/bash

RUN=true

# 設定、変数など
DATE=`date '+%F'`
# FREQ=7.94875 # start freq.
FREQ=7.94875 # start freq.
repeating_time=60 #「2sec * 30回の計測」を 60 セット行う
OPT=''

# python3 venv の起動
source /home/dosue/venv/env1/bin/activate

# LOG に IV や温度などのデータを保存する test_
LOG="/data/ms2840a/blackbody_1hour_preY/blackbody_1hour_preY.log"

# ======================================================================

starttime=`date +%Y-%m-%d-%H:%M:%S`
echo -n "$FREQ, $starttime, " >> $LOG
echo

echo type: test / actual measurement ref_OFF/ON ?
read TYPE
echo -n "$TYPE, " >> $LOG

echo number
read $NUM
echo -n "try_$NUM, " >> $LOG

# echo ref: ON / OFF ?
# read MODE
# echo -n "ref_$MODE, " >> $LOG


# 探索データをここに保存する
SEARCH="/data/ms2840a/blackbody_1hour_preY/$TYPE"

# directry が存在しない場合、以下の directry を新たに生成する
if [ ! -d ${SEARCH} ]; then
    mkdir -p ${SEARCH}
fi

function check_exit_data() {
    DIR0=$1
    CHECK=`python3 check_exist_data.py $FREQ $DIR0`
    # Check overlapping of frequency range
    echo $CHECK
    if [ -n "$CHECK" ]; then
        echo "There is overlapped data for frequency=${FREQ} in ${DIR0}!"
        echo "Please check <FREQ> argument and data directory!"
        echo "If you really want to proceed to measurements, please enter 'Y'."
        read YN
        if [ ! "$YN" == "Y" ]; then
            exit
        fi
    fi
    return 0
}

# LOG に諸情報を保存、追記する
if [ ! -f ${LOG} ]; then
    echo "Create a log file"
    echo -n "# freq[GHz], starttime, endtime" >> $LOG
fi


# ======================================================================



# 説明
# 「2 秒間 FFT を 30 回繰り返すスクリプト」を 60 セット動かし、それぞれ別セットの directry に保存する

check_exit_data $SEARCH
echo
echo '########## Search ##########'
echo 'Please enter if you are ready.'
read enter
echo 'Start search measurement'

for ((TIMES=1; TIMES<=$((repeating_time)); TIMES++)); do

    echo "start ${TIMES} / ${repeating_time}"

    SEARCH_i_times="/data/ms2840a/blackbody_1hour_preY/try_$NUM/$TYPE/set_$TIMES"
    mkdir ${SEARCH_i_times}

    command="python3 run_scanpars_dosue-preY_2MHz.py -m SEARCH --fstart $FREQ -o $SEARCH_i_times $OPT"
    echo $command

    if $RUN; then
        $command
    fi

    echo '########## End of search ##########'
    echo "sleep 5"
    sleep 5


done



endtime=`date +%Y-%m-%d-%H:%M:%S`
echo -n "${endtime}"'\n' >> $LOG


echo ""
echo "END ref check for ${FREQ} GHz!"
echo ""
