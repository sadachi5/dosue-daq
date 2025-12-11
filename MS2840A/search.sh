#!/bin/bash 
# Usage: ./run_dosue-j.sh <PERSON> <FREQ>
# ex) ./run_dosue-j.sh adachi 10.1
# PERSON: your name to record who measured this frequency ex) adachi
# FREQ: start frequency [GHz] ex) 10.1

# Frequency check
if [ $# -lt 2 ]; then
    echo "Please add arguments!"
    echo "Usage: ./run_dosue-j.sh <PERSON> <FREQ>"
    echo "ex) ./run_dosue-j.sh adachi 10.1"
    echo "PERSON: your name to record who measured this frequency ex) adachi"
    echo "FREQ: start frequency [GHz] ex) 10.1"
    exit
fi
PERSON=$1
FREQ=$2

# For running only one-step 
ONE_STEP_ONLY=0
# 1: 77K measurment before
# 2: 300K measurment before
# 3: search measurment
# 4: 300K measurment after
# 5: 77K measurment after
if [ $# -gt 2 ]; then
    ONE_STEP_ONLY=$3
fi

# For test
OPT=''
#OPT=' --noRun'
RUN=true
#RUN=false

source /home/dosue/venv/env1/bin/activate # for python3
DIR=2023-03
#DIR=test
LOG="/data/ms2840a/dosue-j/$DIR.log"
SEARCH="/data/ms2840a/dosue-j/signal_data/$DIR"
YFACTOR_300K_BEFORE="/data/ms2840a/dosue-j/yfactor_300K_ini/$DIR" # 300K before measurement
YFACTOR_77K_BEFORE="/data/ms2840a/dosue-j/yfactor_77K_ini/$DIR" # 77K before measurement
YFACTOR_300K_AFTER="/data/ms2840a/dosue-j/yfactor_300K_fin/$DIR" # 300K after measurement
YFACTOR_77K_AFTER="/data/ms2840a/dosue-j/yfactor_77K_fin/$DIR" # 77K after measurement

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

CHECK=`python3 check_exist_data.py $FREQ $SEARCH`
echo $CHECK
# Check overlapping of frequency range
if [ -n "$CHECK" ]; then
    echo "There is overlapped data for frequency=${FREQ} in ${SEARCH}!"
    echo "Please check <FREQ> argument and data directory!"
    echo "If you really want to proceed to measurements, please enter 'Y'."
    read YN
    if [ ! "$YN" == "Y" ]; then
        exit
    fi
fi

# Initialize log file
if [ ! -f ${LOG} ]; then
    echo "Create a log file"
    echo "# freq[GHz], person, starttime, 300K_temp_before, 300K_temp_after, endtime" >> $LOG
fi

# Measurements (Y-factor & Search & Y-factor)
starttime=`date +%Y-%m-%d-%H:%M:%S`
echo -n "$FREQ, $PERSON, $starttime, " >> $LOG

# 1. Y-factor 77K before
if [ $ONE_STEP_ONLY -eq 0 ] || [ $ONE_STEP_ONLY -eq 1 ]; then
    echo
    echo '########## Y-factor 77K before ##########'
    echo 'Please enter if you prepare for the LN2.'
    read enter
    echo 'Start 77K measurement'
    command="python3 run_scanpars_dosue-j.py -m YFACTOR --fstart $FREQ -o $YFACTOR_77K_BEFORE $OPT"
    echo $command
    if $RUN; then
        $command
    fi
    echo '########## End of Y-factor 77K before ##########'
    echo
fi
./beep.sh

# 2. Y-factor 300K before
if [ $ONE_STEP_ONLY -eq 0 ] || [ $ONE_STEP_ONLY -eq 2 ]; then
    echo
    echo '########## Y-factor 300K before ##########'
    echo 'What is the temperature of the 300K eccosorb?'
    read temp_before
    echo -n "$temp_before, " >> $LOG
    echo 'Please enter if you prepare for the 300K measurement.'
    read enter
    echo 'Start 300K measurement'
    command="python3 run_scanpars_dosue-j.py -m YFACTOR --fstart $FREQ -o $YFACTOR_300K_BEFORE $OPT"
    echo $command
    if $RUN; then
        $command
    fi
    echo '########## End of Y-factor 300K before ##########'
    echo
else
    echo -n ", " >> $LOG
fi
./beep.sh

# 3. Search measurement
if [ $ONE_STEP_ONLY -eq 0 ] || [ $ONE_STEP_ONLY -eq 3 ]; then
    echo
    echo '########## Search ##########'
    echo 'Please enter if you are ready.'
    read enter
    echo 'Start search measurement'
    command="python3 run_scanpars_dosue-j.py -m SEARCH --fstart $FREQ -o $SEARCH $OPT"
    echo $command
    if $RUN; then
        $command
    fi
    echo '########## End of search ##########'
    echo
fi
./beep.sh

# 4. Y-factor 300K after
if [ $ONE_STEP_ONLY -eq 0 ] || [ $ONE_STEP_ONLY -eq 4 ]; then
    echo
    echo '########## Y-factor 300K after ##########'
    echo 'What is the temperature of the 300K eccosorb?'
    read temp_after
    echo -n "$temp_after, " >> $LOG
    echo 'Please enter if you prepare for the 300K measurement.'
    read enter
    echo 'Start 300K measurement'
    command="python3 run_scanpars_dosue-j.py -m YFACTOR --fstart $FREQ -o $YFACTOR_300K_AFTER $OPT"
    echo $command
    if $RUN; then
        $command
    fi
    echo '########## End of Y-factor 300K after ##########'
    echo
else
    echo -n ", " >> $LOG
fi
./beep.sh

# Y-factor 77K after
if [ $ONE_STEP_ONLY -eq 0 ] || [ $ONE_STEP_ONLY -eq 5 ]; then
    echo
    echo '########## Y-factor 77K after ##########'
    echo 'Please enter if you prepare for the LN2.'
    read enter
    echo 'Start 77K measurement'
    command="python3 run_scanpars_dosue-j.py -m YFACTOR --fstart $FREQ -o $YFACTOR_77K_AFTER $OPT"
    echo $command
    if $RUN; then
        $command
    fi
    echo '########## End of Y-factor 77K after ##########'
    echo
fi
./beep.sh

endtime=`date +%Y-%m-%d-%H:%M:%S`
echo "${endtime}" >> $LOG

echo ""
echo "END for ${FREQ} GHz!"
echo ""
