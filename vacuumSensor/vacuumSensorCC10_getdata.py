#!/bin/env python
import os, sys;
import signal;
import serial;
import VacuumSensor;
from time import sleep;
import datetime;
from tzlocal import get_localzone;
import pytz;
 

DEVLOCATION = '/dev/ttyCC-10'; # dosue-daq CC-10 @ 313
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
        line += ' <Vacuum Pressure [Pa]> ';
        f.write(line+'\n');
        f.flush();
        pass;
  except:
      print( 'Error!! Arguments were :');
      print(sys.argv);
      print( 'Error!! Usage: python vacuumSensorCC10_getdata.py <output file> [<device location=/dev/ttyUSB1> [<interval(sec) = 1 [<verbose>=0]]]' );
      exit(1)
      pass

  vs = VacuumSensor.VacuumSensorCC10(devlocation, verbose=verbose);

  while True :
    pressure = vs.readVacuum(); # This function possibly takes some time.
    now      = datetime.datetime.now(timezone);

    # if AM/PM is different between now and start, the job is finished to change the output file.
    if (now.day) != (start.day) : break; 

    line = '';
    line += '{}'.format((int)(now.timestamp()));
    line += ' ';
    line += now.strftime('%Y/%m/%d %H:%M:%S:%f');
    try: 
        line += ' {:f}'.format((float)(pressure)) ;
    except Exception as e:
        print('Warning!! Invalid data obtained (error: {})! --> -1 filled'.format(e))
        line += ' -1';
        pass
    f.write(line+'\n');
    f.flush();
    if ISTEST : 
      print(line);
      break;
    sleep(dt);

    pass; # end of while

  f.close();
  pass;
