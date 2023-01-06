#!/bin/env python
import os, sys;
import signal;
import serial;
import CryomechCPA;
from time import sleep;
import datetime;
from tzlocal import get_localzone;
import pytz;
 

IP_ADDRESS = '169.254.87.107'; 
PORT = 502; 
ISTEST   = False;

## setting for kill signal
def handler(signal, frame):
  print('Exit by kill signal')
  sys.exit(0)
  pass;
signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':

  ip_address = IP_ADDRESS;
  port       = PORT;
  dt      = 60;
  verbose =  0;

  timezone = get_localzone();
  start    = datetime.datetime.now(timezone);

  # get arguments
  # argv[1] : output filename
  # argv[2] : ip address
  # argv[3] : port
  # argv[4] : time duration [sec]
  # argv[5] : verbose
  try:
      if len(sys.argv) < 2 or len(sys.argv) > 6: raise
      try:
        f = open(sys.argv[1], "a")
      except:
        print( 'Error!! Couldn\'t open file {}'.format(sys.argv[1]) );
        exit(1)
        pass;
      if(len(sys.argv) > 2): ip_address  = sys.argv[2];
      if(len(sys.argv) > 3): port        = int(sys.argv[3]);
      if(len(sys.argv) > 4): dt          = float(sys.argv[4])
      if(len(sys.argv) > 5): verbose     = float(sys.argv[5])

      if verbose > 0 :
        print('ip_address  = {}'.format(ip_address ));
        print('port        = {}'.format(port       ));
        print('dt          = {}'.format(dt         ));
        print('verbose     = {}'.format(verbose    ));
        pass;

  except:
      print( 'Error!! Arguments were :');
      print( sys.argv );
      print( 'Error!! Usage: python cryomechCPA_getdata.py '
             '<output file> [<device ip addresss:{}> [<device port:{}> '
             '[<interval(sec):{}> [<verbose:{}>]]]]'
             .format(ip_address, port, dt, verbose) );
      exit(1)
      pass

  cpa = CryomechCPA.CryomechCPA(ip_address, port, verbose=verbose);
  keysWtUnit = cpa.getKeysWtUnit();

  startStr = start.strftime('%Y/%m/%d %H:%M:%S:%f(%Z:%z)');
  line   = '# unix-time {} '.format(startStr);
  for key in keysWtUnit:
    line += ' <{}>'.format(key);
  f.write(line+'\n');
  f.flush();

  while True :
    status = cpa.getStatus();
    now    = datetime.datetime.now(timezone);

    # if AM/PM is different between now and start, the job is finished to change the output file.
    if (now.day) != (start.day) : break; 

    line = '';
    line += '{}'.format((int)(now.timestamp()));
    line += ' ';
    line += now.strftime('%Y/%m/%d %H:%M:%S:%f');
    for value in status:
      line += ' {}'   .format(value) ;
      pass;
    f.write(line+'\n');
    f.flush();
    if ISTEST : break;
    sleep(dt);

    pass; # end of while

  del cpa;
  f.close();
  pass;
