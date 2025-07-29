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
         
devlocation  = '/dev/ttyLS218';

thermometer_name = 'D6077262'
calibcurvefilename = 'cal_data/DT-670-CU-1.4L_D6077262/D6077262.dat'
skip_lines = 3 # skip header lines

channel = 8; # channel number for calibration
curve = (int)('2{}'.format(channel))
# dataformat for LS372: 3=ohm/K (linear), 4=log(ohm)/K(linear), 7=ohm/K (cubic spline)
# dataformat for LS218: 2=V/K, 3=ohm/K, 4=log(ohm)/K
dataformat = 2
templimit =  330 # K
posneg = 1 # curve coeff. + or - (1: negative, 2: positive)

ssleep = sleep(0.1);
defaultverbose = True;


## Main ##
calibfile = open(calibcurvefilename, 'r');

calibdata    = [];

# get calibration curve
for i, line in enumerate(calibfile) :
  # skip headers
  if skip_lines > i: continue
  # skip comments
  if line.startswith('#') or len(line)==0 : continue

  line = line.strip();
  columns = line.split();
  
  data={}
  data['temp'] = (float)(columns[0]);
  data['raw'] = (float)(columns[1]);
  calibdata.append(data)
  pass;

print( calibdata );

# intialize serial communication
ls = lakeshore.Lakeshore(devlocation);

# delete calibration curve
ls.deletecalibration(channel)
# write calibration curve
ls.addcalibration(channel, name=thermometer_name, serialnumber=thermometer_name, dataformat=dataformat, templimit=templimit, posneg=posneg);
for i, data in enumerate(calibdata):
  temp = data['temp'];
  raw = data['raw'];
  ls.setcalibration(channel, temp, raw, i); 
  pass;
  
ls.printcalibration(channel, imax=71, doPrint=True);

# set the calibration curve to the channel
ls.changecalibrationcurve(channel, curve);
ls.printcalibration(channel, imax=71, doPrint=True);
