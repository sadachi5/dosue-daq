#!/bin/env python
import os, sys;
import datetime;
       
this_dir = os.path.dirname(os.path.abspath(__file__))
run_script = '{}/cryomechCPA_getdata.py'.format(this_dir);
outdirectory = '/data/ajariCryoPTC';
ip_address = '169.254.87.107'; # Ajari Cryo PTC IP address
port = 502; # Ajari Cryo PTC port
dt = 10; # data aqcuisition period [sec]

if __name__ == '__main__':

  isTest = False;
  if len(sys.argv)>1 : isTest = True;

  now = datetime.datetime.now();
  nowStr = now.strftime('%Y-%m-%d');
  outputfilename = '{}/data_{}.dat'.format( outdirectory, nowStr );
  cmd = r'python3 {} {} {} {} {}'.format( run_script, outputfilename, ip_address, port, dt );
  print(cmd);
  if not isTest : os.system( cmd );

  pass;
