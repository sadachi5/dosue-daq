#!/bin/env python
import os, sys;
import datetime;
       
this_dir = os.path.dirname(os.path.abspath(__file__))
run_script = '{}/vacuumSensorTPG361_getdata.py'.format(this_dir);
outdirectory = '/data/vacuumSensorTPG361_SN44879560'
devlocation = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AB0LD096-if00-port0' # 027 TPG-361 SN44879560
#outdirectory = '/data/vacuumSensorTPG361';
#devlocation = '/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_AC01UUAI-if00-port0'; # tandem TPG-361
#outdirectory = '/data/test';
#devlocation = '/dev/ttyUSB2';
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
