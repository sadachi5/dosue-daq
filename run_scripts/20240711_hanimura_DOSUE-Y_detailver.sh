# DOSUE-Y IF test at 4K
. /home/dosue/venv/env1/bin/activate

# 4GHz
echo "Is it OK and prepared for 300K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_300K_4GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 8.4e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "Is it OK and prepared for 77K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_77K_4GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 8.4e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "4.0GHz finished..."
echo "next: 6.3GHz"

# 6.3GHz
echo "Is it OK and prepared for 300K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_300K_6.3GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 6.3e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "Is it OK and prepared for 77K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_77K_6.3GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 6.3e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "6.3GHz finished..."
echo "next: 8.4->4.0GHz"

# 8.4GHz
echo "Is it OK and prepared for 300K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_300K_4GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 4.0e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "Is it OK and prepared for 77K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_77K_4GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 8.4e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "8.4GHz finished..."
echo "next: 9.0GHz"

# 9.0GHz
echo "Is it OK and prepared for 300K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_300K_9.0GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 9.0e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "Is it OK and prepared for 77K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_77K_9.0GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 9.0e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "9.0GHz finished..."
echo "next: 10.0GHz"

# 10.0GHz
echo "Is it OK and prepared for 300K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_300K_10.0GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 10.0e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "Is it OK and prepared for 77K measurement? [y/n]"
read YN

if [ $YN = "y" ]; then
  python3 ../MS2840A/MS2840A.py -f DOSUE-Y_test_SWEEP_detailver_77K_10.0GHz_1MHz_RBW1kHz_1sec_100loop_test1 -m 'SWEEP' -s 10.0e+9 -w 1e+6 -r 1000 -n 100 --att 0 --nRun 1 --overwrite
fi

echo "10.0GHz finished..."
