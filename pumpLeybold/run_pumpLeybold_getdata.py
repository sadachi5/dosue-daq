#!/bin/env python
import os, sys;
import datetime;
       
this_dir = os.path.dirname(os.path.abspath(__file__))
run_script = '{}/pumpLeybold_getdata.py'.format(this_dir);
outdirectory = '/data/pumpLeybold';
#devlocation = '192.168.11.4'; # Leybold pump system
devlocation = '192.168.215.221'; # Leybold pump system from 2025/7/7 @ tandem for JSAT
dt = 10; # data aqcuisition period [sec]

if __name__ == '__main__':

  isTest = False;
  if len(sys.argv)>1 : isTest = True;

  now = datetime.datetime.now();
  nowStr = now.strftime('%Y-%m-%d');
  outputfilename = '{}/data_{}.dat'.format( outdirectory, nowStr );
  cmd = r'python3 {} {} {} {}'.format( run_script, outputfilename, devlocation, dt );
  print(cmd);
  if not isTest : os.system( cmd );

  pass;
