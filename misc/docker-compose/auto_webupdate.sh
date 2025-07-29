#!/bin/bash
# data is synchronized automatically to the local directory
DATALOCATION=/data
DATALOCATION_TANDEM=/mnt/cmb-tandem/data
HTMLLOCATION=/home/adachi/hep_web/grafana
TEMPERATURE_PLOT=/data/analysis/adachi/dosue-analysis/Temperature/figure/temperature_compare.png

#while [ true ]
#do
  echo '### Sart Updating ###';
  echo "date : `date`";
  #now=`ssh tandem -C "LANG=C date"`;
  now=`LANG=C date`;
  date=`date +%Y-%m-%d`;

  for page in "index.html";
  do
    echo "update numbers in $page"
    ssh hepsrv -C "sed -i \"s%Current values (Update:.*)%Current values (Update:${now})%\" ${HTMLLOCATION}/${page}"

    ## Lakeshore 218 ##
    echo "$DATALOCATION/lakeshore218/data_${date}.dat";
    vals=`tail -n 1 $DATALOCATION/lakeshore218/data_${date}.dat`
    echo $vals;
    vals=`echo ${vals} | awk -F' |:' '{printf("%s %s:%s:%s %s %.3fK %s %.3fK %s %.3fK %s %.4fK %s %.3fK %s %.3fK %s %.3fK %s %.3fK", $2, $3, $4, $5, $6, $7, $9, $10, $12, $13, $15, $16, $18, $19, $21, $22, $24, $25, $27, $28)}'`
    echo $vals;
    ssh hepsrv -C "sed -i \"s%Temperature (Lakeshore 218): .*</li>%Temperature (Lakeshore 218): <br> ${vals} </li>%\" ${HTMLLOCATION}/${page}"
 
    ## CC-10 ##
    echo "$DATALOCATION/vacuumSensorCC10/data_${date}.dat";
    vals=`tail -n 1 $DATALOCATION/vacuumSensorCC10/data_${date}.dat`
    echo $vals;
    vals=`echo ${vals} | awk -F' |:' '{printf("%s %s:%s:%s %sPa", $2, $3, $4, $5, $7)}'`
    echo $vals;
    ssh hepsrv -C "sed -i \"s%Vacuum pressure (CC-10): .*</li>%Vacuum pressure (CC-10): <br>${vals} </li>%\" ${HTMLLOCATION}/${page}"

    ## TPG361_SN44879560 ##
    echo "$DATALOCATION/vacuumSensorTPG361_SN44879560/data_${date}.dat";
    vals=`tail -n 1 $DATALOCATION/vacuumSensorTPG361_SN44879560/data_${date}.dat`
    echo $vals;
    vals=`echo ${vals} | awk -F' |:' '{printf("%s %s:%s:%s %sPa", $2, $3, $4, $5, $7)}'`
    echo $vals;
    ssh hepsrv -C "sed -i \"s%Vacuum pressure (TPG361_SN44879560): .*</li>%Vacuum pressure (TPG361_SN44879560): <br>${vals} </li>%\" ${HTMLLOCATION}/${page}"

    # Tandem #
    ssh hepsrv -C "sed -i \"s%Current values (Update@Tandem:.*)%Current values (Update@Tandem:${now})%\" ${HTMLLOCATION}/${page}"
    ## Lakeshore 218 ##
    echo "$DATALOCATION_TANDEM/lakeshore218/data_${date}.dat";
    vals=`tail -n 1 $DATALOCATION_TANDEM/lakeshore218/data_${date}.dat`
    echo $vals;
    vals=`echo ${vals} | awk -F' |:' '{printf("%s %s:%s:%s %s %.3fK %s %.3fK %s %.3fK %s %.4fK %s %.3fK %s %.3fK %s %.3fK %s %.3fK", $2, $3, $4, $5, $6, $7, $9, $10, $12, $13, $15, $16, $18, $19, $21, $22, $24, $25, $27, $28)}'`
    echo $vals;
    ssh hepsrv -C "sed -i \"s%Temperature (Tandem Lakeshore 218): .*</li>%Temperature (Tandem Lakeshore 218): <br> ${vals} </li>%\" ${HTMLLOCATION}/${page}"
 
    ## Leybold ##
    echo "$DATALOCATION_TANDEM/pumpLeybold/data_${date}.dat";
    vals=`tail -n 1 $DATALOCATION_TANDEM/pumpLeybold/data_${date}.dat`
    echo $vals;
    vals=`echo ${vals} | awk -F' |:' '{printf("%s %s:%s:%s %s Pa %s Hz", $2, $3, $4, $5, $7, $11)}'`
    echo $vals;
    ssh hepsrv -C "sed -i \"s%Vacuum pressure (Tandem Leybold): .*</li>%Vacuum pressure (Tandem Leybold): <br>${vals} </li>%\" ${HTMLLOCATION}/${page}"

    ## Temperature plot ##
    rsync -ruavv $TEMPERATURE_PLOT hepsrv:~/hep_web/grafana/temperature.png


  done


#  echo "sleep";
#  echo "";
#  echo "";
#  sleep 60;
#done
