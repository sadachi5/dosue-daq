# DOSUE-Y SIS test at 4K

start="3e+9"
width="10e+9"
rbw="10e+6"
nLoop=1
nRun=10
LO=210
#prefix="DOSUE-Y_Y-factor"
prefix="DOSUE-Y_Y-factor2"
ONLYplot=true
#ONLYplot=false

echo 'Voltage ? [mV]'
read volt
echo 'Current ? [mV]'
read curr

volt=`python -c "print(f'{$volt/100.:.3f}')"`
curr=`python -c "print(f'{$curr/10.:.1f}')"`

#prefix="test"
suffix="${LO}GHz_${volt}mV-${curr}uA"
#dateStr=`date +%F`
dateStr=2022-09-27
outdir="/data/ms2840a/${dateStr}"
logfile="${outdir}/data/${prefix}_${suffix}.log"

echo "LO = ${LO} + 0.3 GHz"
echo "Voltage = ${volt} mV"
echo "Current = ${curr} uA"
echo "suffix = ${suffix}"
echo "logfile = ${logfile}"

if ${ONLYplot} ; then
   # plot y-factor
   python3 ./python/yfactor_diff.py \
       --outdir ${outdir}/figure \
       --outname ${prefix}_${suffix}_0-0_yfactor.pdf \
       --input1 ${outdir}/data/${prefix}_${suffix}_300K_0.dat \
       --input2 ${outdir}/data/${prefix}_${suffix}_77K_0.dat \

else
    echo 'Blackbody temperature? [deg.]'
    read temp
    echo "300K temperature = ${temp} deg"

    echo "Is it OK and prepared for 300K measurement? [y/n]"
    read YN

    if [ $YN = "y" ]; then

        echo 'Start 300K measurement'
        python3 ../MS2840A/MS2840A.py -f ${prefix}_${suffix}_300K -m 'SWEEP' -s $start -w $width -r $rbw -n ${nLoop} --att 0 --nRun ${nRun}

        echo "Did you prepared for 77K measurement? [Please push enter!]"
        read

        python3 ../MS2840A/MS2840A.py -f ${prefix}_${suffix}_77K -m 'SWEEP' -s $start -w $width -r $rbw -n ${nLoop} --att 0 --nRun ${nRun}

        echo 'After Voltage ? [mV]'
        read volt2
        echo 'After Current ? [mV]'
        read curr2

        volt2=`python -c "print(f'{$volt2/100.:.3f}')"`
        curr2=`python -c "print(f'{$curr2/10.:.1f}')"`

        echo "filename_300K: ${prefix}_${suffix}_300K" > $logfile
        echo "filename_77K: ${prefix}_${suffix}_77K" > $logfile
        echo "LO: ${LO} GHz + 0.3 GHz" >> $logfile
        echo "voltage: ${volt} mV" >> $logfile
        echo "current: ${curr} uA" >> $logfile
        echo "BB_temperature: ${temp} deg" >> $logfile
        echo "After voltage: ${volt2} mV" >> $logfile
        echo "After current: ${curr2} uA" >> $logfile
        echo "" >> $logfile
        echo "Spectrum_analyzer_settings" >> $logfile
        echo "start_frequency: ${start} Hz" >> $logfile
        echo "frequency_width: ${width} Hz" >> $logfile
        echo "RBW: ${rbw} Hz" >> $logfile
        echo "nLoop: ${nLoop}" >> $logfile
        echo "nRun: ${nRun}" >> $logfile

        # plot y-factor
        echo "" >> $logfile
        echo "Yfactor" >> $logfile
        python3 ./python/yfactor_diff.py \
            --outdir ${outdir}/figure \
            --outname ${prefix}_${suffix}_0-0_yfactor.pdf \
            --input1 ${outdir}/data/${prefix}_${suffix}_300K_0.dat \
            --input2 ${outdir}/data/${prefix}_${suffix}_77K_0.dat \
            >> $logfile
        cat $logfile
    fi
fi
