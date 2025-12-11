# 説明
# dosue-preY による 7.95 GHz 近傍 (2.5 MHz 帯域) の測定に使用した shellscripi である
# 2024/12/05 作成 by hanimura

# =========== step について =========================================
#
# (1) SIS mixer bias V, I を記録
# (2-a) 300 K の黒体を窓に設置し、放射温度計で温度を測定し記録
# (2-b) 300 K 黒体のパワーを測定する (今回は 2 秒 * 10 回)
# (2-c) 測定後、300 K 黒体の温度を再測定する (a, c で測った温度の平均を黒体の温度とみなす)
# (3) 77K の黒体を設置し、測定する（水分がついていないか確認）
# (4) 探索測定を開始する。
#   今回は 2 秒間の FFT を 1800 回繰り返す。
#   30 回 60 秒間ごとにデータの保存先を別のディレクトリに変更する
#   (FFT が途中で停止した時、どこで止まったか、どこから再開すればいいかを確認しやすくするため）。
#   探索測定が終了したら、
# (5) SIS mixer bias V, I を記録
# (6-a) 300 K の黒体を窓に設置し、放射温度計で温度を測定し記録
# (6-b) 300 K 黒体のパワーを測定する (今回は 2 秒 * 10 回)
# (6-c) 測定後、300 K 黒体の温度を再測定する (a, c で測った温度の平均を黒体の温度とみなす)
# (7) 77K の黒体を設置し、測定する（水分がついていないか確認）
# 探索終了
#
# ==================================================================

#!bin/bash

RUN=true

# 設定、変数など
# DIR=test5_`date '+%F'`
# DIR=`date '+%F'` # 本番はこっち
DIR=retry_`date '+%F'` # 本番はこっち
FREQ=7.94875 # start freq.
repeating_time=60 #「2sec * 30回の計測」を 60 セット行う
OPT=''

# python3 venv の起動
source /home/dosue/venv/env1/bin/activate

# LOG に IV や温度などのデータを保存する test_
LOG="/data/ms2840a/dosue-preY_2MHz/$DIR.log"

# 探索データをここに保存する
SEARCH="/data/ms2840a/dosue-preY_2MHz/signal_data/$DIR"

# Caliubration: 300K/77K, before/after measurement をここに保存する
YFACTOR_300K_BEFORE="/data/ms2840a/dosue-preY_2MHz/yfactor_300K_ini/$DIR"
YFACTOR_77K_BEFORE="/data/ms2840a/dosue-preY_2MHz/yfactor_77K_ini/$DIR"
YFACTOR_300K_AFTER="/data/ms2840a/dosue-preY_2MHz/yfactor_300K_fin/$DIR"
YFACTOR_77K_AFTER="/data/ms2840a/dosue-preY_2MHz/yfactor_77K_fin/$DIR"

# directry が存在しない場合、以下の directry を新たに生成する
if [ ! -d ${SEARCH} ]; then
    mkdir ${SEARCH}
fi
if [ ! -d ${YFACTOR_300K_BEFORE} ]; then
    mkdir ${YFACTOR_300K_BEFORE}
fi
if [ ! -d ${YFACTOR_300K_AFTER} ]; then
    mkdir ${YFACTOR_300K_AFTER}
fi
if [ ! -d ${YFACTOR_77K_BEFORE} ]; then
    mkdir ${YFACTOR_77K_BEFORE}
fi
if [ ! -d ${YFACTOR_77K_AFTER} ]; then
    mkdir ${YFACTOR_77K_AFTER}
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
    echo "# freq[GHz], starttime, bias_V_before[mV], bias_I_before[µA], 300K_temp_before, 300K_temp_before2, bias_V_after[mV], bias_I_after[µA], 300K_temp_after, 300K_temp_after2, endtime" >> $LOG
fi



# ======================================================================

# (1)(2) Y-factor 300K before
starttime=`date +%Y-%m-%d-%H:%M:%S`
echo -n "$FREQ, $starttime, " >> $LOG
echo
echo '########## bias IV measurement ##########'
echo 'How much is the Bias Voltage[mV] ?'
read bias_V_before
echo -n "$bias_V_before, " >> $LOG

echo
echo 'How much is the Bias Current[µA] ?'
read bias_I_before
echo -n "$bias_I_before, " >> $LOG

echo
echo 'PLL OK ?'
read YN


check_exit_data $YFACTOR_300K_BEFORE
echo
echo '########## Y-factor 300K before ##########'
echo 'How much is the temperature of the 300K eccosorb (after 300K measurement)?'
read temp_before
echo -n "$temp_before, " >> $LOG

echo 'Please enter if you prepare for the 300K eccoroeb.'
read enter
echo 'Start 300K measurement'
command="python3 run_scanpars_dosue-preY_2MHz.py -m YFACTOR --fstart $FREQ -o $YFACTOR_300K_BEFORE $OPT"
echo $command
if $RUN; then
    $command
fi
echo '########## End of Y-factor 300K before ##########'
echo

./beep.sh

echo 'How much is the temperature of the 300K eccosorb (after 300K measurement)?'
read temp_before
echo -n "$temp_before, " >> $LOG


# ======================================================================

# (3) Y-factor 77K before

check_exit_data $YFACTOR_77K_BEFORE
echo
echo '########## Y-factor 77K before ##########'
echo 'Please enter if you prepare for the LN2.'
read enter
echo 'Start 77K measurement'
command="python3 run_scanpars_dosue-preY_2MHz.py -m YFACTOR --fstart $FREQ -o $YFACTOR_77K_BEFORE $OPT"
echo $command
if $RUN; then
    $command
fi
echo '########## End of Y-factor 77K before ##########'
echo

./beep.sh


# ======================================================================

# (4) Search Measurement

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

    SEARCH_i_times="/data/ms2840a/dosue-preY_2MHz/signal_data/$DIR/set_$TIMES"
    mkdir ${SEARCH_i_times}

    command="python3 run_scanpars_dosue-preY_2MHz.py -m SEARCH --fstart $FREQ -o $SEARCH_i_times $OPT"
    echo $command

    if $RUN; then
        $command
    fi

    echo '########## End of search ##########'
    echo

    ./beep.sh

done


# ======================================================================

# (5)(6) Y-factor 300K after
echo '########## bias IV measurement ##########'
echo 'How much is the Bias Voltage[mV] ?'
read bias_V_after
echo -n "$bias_V_after, " >> $LOG

echo
echo 'How much is the Bias Current[µA] ?'
read bias_I_after # 12/09 に発見 before　になっていた
echo -n "$bias_I_after, " >> $LOG


check_exit_data $YFACTOR_300K_AFTER
echo
echo '########## Y-factor 300K after ##########'
echo 'How much is the temperature of the 300K eccosorb (after 300K measurement)?'
read temp_after
echo -n "$temp_after, " >> $LOG

echo 'Please enter if you prepare for the 300K eccoroeb.'
read enter
echo 'Start 300K measurement'
command="python3 run_scanpars_dosue-preY_2MHz.py -m YFACTOR --fstart $FREQ -o $YFACTOR_300K_AFTER $OPT"
echo $command
if $RUN; then
    $command
fi
echo '########## End of Y-factor 300K after ##########'
echo

./beep.sh

echo 'How much is the temperature of the 300K eccosorb (after 300K measurement)?'
read temp_after
echo -n "$temp_after, " >> $LOG


# ======================================================================

# (7) Y-factor 77K after

check_exit_data $YFACTOR_77K_AFTER
echo
echo '########## Y-factor 77K after ##########'
echo 'Please enter if you prepare for LN2.'
read enter
echo 'Start 77K measurement'

command="python3 run_scanpars_dosue-preY_2MHz.py -m YFACTOR --fstart $FREQ -o $YFACTOR_77K_AFTER $OPT"

echo $command
if $RUN; then
    $command
fi
echo '########## End of Y-factor 77K after ##########'
echo

./beep.sh

endtime=`date +%Y-%m-%d-%H:%M:%S`
echo "${endtime}" >> $LOG


echo ""
echo "END for ${FREQ} GHz!"
echo ""
