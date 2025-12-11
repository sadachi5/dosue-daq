# DOSUE-Y IF test at 4K
. /home/dosue/venv/env1/bin/activate

echo "Is it OK and prepared for 300K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_300K_4GHz_1MHz_RBW1kHz_1sec_100loop_1 -m 'SWEEP' -s 4e+9 -w 1e+6 -r 300 -t 1 --att 0 --nRun 1 --overwrite
fi

echo "Is it OK and prepared for 77K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_77K_4GHz_1MHz_RBW1kHz_1sec_100loop_1 -m 'SWEEP' -s 4e+9 -w 1e+6 -r 300 -t 1 --att 0 --nRun 1 --overwrite
fi

echo "8.4GHz finished..."
