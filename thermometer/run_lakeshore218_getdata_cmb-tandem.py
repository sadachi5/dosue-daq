#!/bin/env python3
import os, sys;
import datetime;
       
this_dir = os.path.dirname(os.path.abspath(__file__))
run_script = '{}/lakeshore218_getdata.py'.format(this_dir);
outdirectory = '/data/lakeshore218';
devlocation  = '/dev/serial/by-id/usb-FTDI_USB_HS_SERIAL_CONVERTER_FTS9SGH5-if00-port0'; # lakeshore218 # cmb-tandem (Ajari-cryo)
dt = 1

if __name__ == '__main__':

  isTest = False;
  if len(sys.argv)>1 : isTest = True;

  now = datetime.datetime.now();
  #isAM = (now.hour<12);
  #nowStr = now.strftime('%Y-%m-%d{}'.format( 'AM' if isAM else 'PM') );
  nowStr = now.strftime('%Y-%m-%d');
  outputfilename = '{}/data_{}.dat'.format( outdirectory, nowStr );
  cmd = r'python3 {} {} {} {}'.format( run_script, outputfilename, devlocation, dt );
  print(cmd);
  if not isTest : os.system( cmd );

  pass;
