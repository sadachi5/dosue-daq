# DOSUE-Y IF test at 4K
#!bin/bash
. /home/dosue/venv/env1/bin/activate
start="3e+9"
width="10e+9"
rbw="10e+6"
nLoop=100
nRun=1

echo "How many times do you want to measure?"
read repeating_time


echo "starting LO[GHz] = ?"
read LO
echo "OK, you can measure from $((LO)) to $((LO+repeating_time-1))."

sleep 1

echo "... loading ..."
sleep 1

for ((i=1; i<$((repeating_time+1)); i++)); do

echo "Anapico ON! $((LO+i-1)) GHz (˙꒳​˙ᐢ)push!"
python ../APSYN420/APSYN420.py --on -f $(((LO+i-1)*1000000000/18))

echo "Is it OK and prepared for 300K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
    echo "Please Wait for 20 sec (u_u)...zzZ"

    total=20
    # プログレスバー全体の幅
    box_width=40
    # for i in $(seq 1 ${total}); do
    for ((j=1; j<$((total+1)); j++)); do

    # 処理を実行
    sleep 1

    # 現在のバーの横幅
    bar_width=$(( box_width * j / total ))

    # バーの空きスペース
    space=$(( box_width - bar_width ))

    # 現在の割合
    percent=$(( j * 100 / total ))

    # バーを出力
    printf '\r['
    yes "#" | head -n "${bar_width}" | tr -d "\n"
    yes " " | head -n "${space}" | tr -d "\n"
    printf "] %s%%" "${percent}"
    done

    printf '..done\n'

    echo 'Start 300K measurement!'

    python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_NoiseTest_LO$((LO+i-1))_300K -m 'SWEEP' -s $start -w $width -r $rbw -n ${nLoop} --att 0 --nRun ${nRun} --overwrite

    echo "Taking a break (u_u)...zzZ"
    sleep 2
fi

echo "~ Next measurement! ~"
echo "Is it OK and prepared for 77K measurement? [y/n]"
read YN2

if [ $YN2 = "y" ]; then
    echo "Please Wait for 20 sec (^ω^)v"

    total=20
    # プログレスバー全体の幅
    box_width=40
    # for i in $(seq 1 ${total}); do
    for ((j=1; j<$((total+1)); j++)); do

    # 処理を実行
    sleep 1

    # 現在のバーの横幅
    bar_width=$(( box_width * j / total ))

    # バーの空きスペース
    space=$(( box_width - bar_width ))

    # 現在の割合
    percent=$(( j * 100 / total ))

    # バーを出力
    printf '\r['
    yes "#" | head -n "${bar_width}" | tr -d "\n"
    yes " " | head -n "${space}" | tr -d "\n"
    printf "] %s%%" "${percent}"
    done

    printf '..done\n'

    echo "Start 77K measurement!"

    python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_NoiseTest_LO$((LO+i-1))_77K -m 'SWEEP' -s $start -w $width -r $rbw -n ${nLoop} --att 0 --nRun ${nRun} --overwrite

    sleep 2
    echo "OK, finish it!"

    sleep 1
fi

done

python3 ../APSYN420/APSYN420.py --off

echo "Don't Forget Stop SIS Bias Voltage!!!!! (>_<)"
