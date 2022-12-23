#!/bin/env python
import os, sys;
import datetime;
       
this_dir = os.path.dirname(os.path.abspath(__file__))
run_script = '{}/vacuumSensorTPG361_getdata.py'.format(this_dir);
outdirectory = '~/data/vacuumSensorTPG361';
devlocation = '/dev/serial/by-id/usb-FTDI_USB_HS_SERIAL_CONVERTER_FTT37E2F-if00-port0'; # dosue-pi TPG-261
dt = 60; # data aqcuisition period [sec]

if __name__ == '__main__':

  isTest = False;
  if len(sys.argv)>1 : isTest = True;

  now = datetime.datetime.now();
  nowStr = now.strftime('%Y-%m-%d');
  outputfilename = '{}/data_{}.dat'.format( outdirectory, nowStr );
  cmd = r'python {} {} {} {}'.format( run_script, outputfilename, devlocation, dt );
  print(cmd);
  if not isTest : os.system( cmd );

  pass;
