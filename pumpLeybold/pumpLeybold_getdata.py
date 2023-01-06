#!/bin/env python
import os, sys;
import signal;
from pumpLeybold import read_pump 
from time import sleep;
import datetime;
from tzlocal import get_localzone;
import pytz;
 

DEVLOCATION = '192.168.11.4'; # Leybold pump system
ISTEST   = False;

## setting for kill signal
def handler(signal, frame):
  print('Exit by kill signal')
  sys.exit(0)
  pass;
signal.signal(signal.SIGINT, handler)

if __name__ == '__main__':

  devlocation = DEVLOCATION;
  dt      = 60;
  verbose =  0;

  timezone = get_localzone();
  start    = datetime.datetime.now(timezone);

  # get arguments
  # argv[1] : output filename
  # argv[2] : devlocation
  # argv[3] : time duration [sec]
  # argv[4] : verbose
  try:
      if len(sys.argv) < 2 or len(sys.argv) > 5: raise
      add = False
      if os.access(sys.argv[1], os.R_OK): add = True; # when continue to write
      if not os.path.isfile(sys.argv[1]): add = True; # when create a new file
      try:
        f = open(sys.argv[1], "a")
      except:
        print( 'Error!! Couldn\'t open file {}'.format(sys.argv[1]) );
        exit(1)
        pass;
      if(len(sys.argv) > 2): devlocation = sys.argv[2];
      if(len(sys.argv) > 3): dt          = float(sys.argv[3])
      if(len(sys.argv) > 4): verbose     = float(sys.argv[4])

      if verbose > 0 :
        print('devlocation = {}'.format(devlocation));
        print('dt          = {}'.format(dt         ));
        print('verbose     = {}'.format(verbose    ));
        pass;

      if add :
        startStr = start.strftime('%Y/%m/%d %H:%M:%S:%f(%Z:%z)');
        line   = '# unix-time {} '.format(startStr);
        line += ' <Pressure1 [Pa]> ';
        line += ' <Pressure2 [Pa]> ';
        line += ' <Power [W]> ';
        line += ' <Current [A]> ';
        line += ' <Frequency [Hz]> ';
        line += ' <Temperature [deg.]> ';
        f.write(line+'\n');
        f.flush();
        pass;
  except:
      print( 'Error!! Arguments were :');
      print( sys.argv );
      print( 'Error!! Usage: python pumpLeybold_getdata.py <output file> [<device ip address=192.168.11.4> [<interval(sec) = 1 [<verbose>=0]]]' );
      exit(1)
      pass

  while True :
    pars = read_pump(ip = devlocation, timezone=timezone);
    now = pars['time']

    # if AM/PM is different between now and start, the job is finished to change the output file.
    if (now.day) != (start.day) : break; 

    line = '';
    line += '{}'.format((int)(now.timestamp()));
    line += ' ';
    line += now.strftime('%Y/%m/%d %H:%M:%S:%f');
    line += ' {}'   .format(pars['pressure1']) ;
    line += ' {}'   .format(pars['pressure2']) ;
    line += ' {}'   .format(pars['power']) ;
    line += ' {}'   .format(pars['current']) ;
    line += ' {}'   .format(pars['frequency']) ;
    line += ' {}'   .format(pars['temperature']) ;
    f.write(line+'\n');
    f.flush();
    if ISTEST : 
      print(line);
      break;
    sleep(dt);

    pass; # end of while

  f.close();
  pass;
