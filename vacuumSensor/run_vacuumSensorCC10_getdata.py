#!/bin/env python
import os, sys;
import datetime;
       
this_dir = os.path.dirname(os.path.abspath(__file__))
run_script = '{}/vacuumSensorCC10_getdata.py'.format(this_dir);
outdirectory = '/data/vacuumSensorCC10';
devlocation = '/dev/ttyCC-10'; # tandem CC-10
dt = 10; # data aqcuisition period [sec]

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
