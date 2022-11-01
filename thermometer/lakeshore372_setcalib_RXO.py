#!/bin/env python
import os, sys;
import serial;
import json;
import numpy as np;
import array;
from time import sleep;
import datetime;
import lakeshore;

#########################################################
# NEED TO REMOVE COMMENT OUT TO SET CALIBRATION CURVE!! #
#########################################################
         
devlocation  = '169.254.235.124,255.255.0.0,7777'; # lakeshore372

#calibcurvefilename = 'RXO_calibrationcurve_Abe.txt';
calibcurvefilename = 'RXO_calibrationcurve_Abe_to2K.txt';

channels = [1]; # channel number for calibration

ssleep = sleep(0.1);

defaultverbose = True;



calibfile = file(calibcurvefilename, 'r');


calibdata    = [];
labelcolumns = [];
nTemp     = -1;
nChannels = [];

# get calibration curve
for line in calibfile :
  line = line.strip();
  if line.startswith('#') : 
    labelcolumns = line.lstrip('#').split();
    for i,label in enumerate(labelcolumns) :
      if np.any( [ (search in label) for search in ['Temp', 'temp'] ] ): nTemp = i;
      for c in channels :
        if np.any( [ (search in label) for search in ['CH{}'.format(c), 'ch{}'.format(c)] ] ): nChannels.append(i);
        pass;
      pass;
    if nTemp<0 or nChannels<len(channels) :
      print('Error!! Could not get temperature or channel columns!');
      print('        Reqired channels : ',channels);
      print('        nTemp     = {}'.format(nTemp)               );
      print('        nChannels = {}'.format(','.join(nChannels)) );
      sys.exit(1);
      pass;
    print('nTemp     = {}'.format(nTemp    ));
    print('nChannels = ,',nChannels         );
    pass;
    
  if line.startswith('#') or len(line)==0 : continue;

  columns = line.split();
  
  data = {};
  data['temp'] = (float)(columns[nTemp]);
  for i, c in enumerate(channels) : data[c] = (float)(columns[nChannels[i]]);

  calibdata.append(data);
  
  pass;

print( calibdata );

# intialize serial communication
devTmp = devlocation.split(',');
devlocationDict = {'ip':devTmp[0], 'mask':devTmp[1], 'port':(int)(devTmp[2]) };
ls = lakeshore.Lakeshore(devlocationDict);

# write calibration curve
for c in channels :
  posneg = 2 if (calibdata[0][c]-calibdata[-1][c])*(calibdata[0]['temp']-calibdata[-1]['temp'])>0 else 1 ;
  print( 'posneg = {}'.format(posneg) );
  #ls.addcalibration(c, name='channel{}'.format(c), dataformat=3, templimit=500, posneg=posneg);
  ls.addcalibration(c, name='channel{}'.format(c), dataformat=3, templimit=500, posneg=posneg);
  pass;
for i, data in enumerate(calibdata) :
  temp = data['temp'];
  for c in channels :
    resist = data[c];
    ls.setcalibration(c, temp, resist, i); # if do set calibration after addcalibration(), posneg of 1 is changed to 2, unintentionally.
  pass;
  
ls.printcalibration(c, doPrint=True);

# set the calibration curve to the channel
for c in channels :
  ls.changecalibrationcurve( c, (int)('2{}'.format(c)) );
  pass;

ls.getcalibrationcurve( c, doPrint=True );
