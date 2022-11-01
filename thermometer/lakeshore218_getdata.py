#!/bin/env python
import os, sys;
import serial;
import lakeshore;
from time import sleep;
import datetime;
       
devlocation = '/dev/ttyUSB0';
isTest = False;


if __name__ == '__main__':

    devlocation = "/dev/ttyUSB1";
    dt = 60
    channels = [1,2,3,4,5,6,7,8];
 
    start = datetime.datetime.now();
 
    try:
        if len(sys.argv) < 2 or len(sys.argv) > 4: raise
        add = False
        if os.access(sys.argv[1], os.R_OK): add = True; # when continue to write
        if not os.path.isfile(sys.argv[1]): add = True; # when create a new file
        try:
            f = open(sys.argv[1], "a")
        except:
            print( 'Error!! Couldn\'t open file {}'.format(sys.argv[1]) );
            exit(1)
            pass;
        if add :
            startStr = start.strftime('%Y/%m/%d %H:%M:%S (Unix time)');
            line   = '# unix-time {} '.format(startStr);
            for c in channels :
                line += ' {}ch <Temp[K]> <Raw value>'.format(c);
                pass;
            f.write(line+'\n');
            f.flush();
            pass;
        if(len(sys.argv) > 2): devlocation = sys.argv[2];
        if(len(sys.argv) > 3): dt          = int(sys.argv[3])
    except:
        print( 'Error!! Arguments were :');
        print( sys.argv );
        print( 'Error!! Usage: python lakeshore218_getdata.py <output file> [<device location=/dev/ttyUSB1> [<interval(sec) = 60>]]' );
        exit(1)
        pass
 
    ls = lakeshore.Lakeshore(devlocation);
 
    while True :
 
        now  = datetime.datetime.now();
        ## if AM/PM is different between now and start, the job is finished to change the output file.
        #if (now.hour>=12) != (start.hour>=12) : break; 
        if (now.day) != (start.day) : break; 
       
        data_K = ls.gettemps(channels, "K")
        data_S = ls.gettemps(channels, "S")
        line = '';
       
        line += '{}'.format(int(now.timestamp()));
        line += ' ';
        line += now.strftime('%Y/%m/%d %H:%M:%S');
        for i, c in enumerate(channels) :
            try: 
                line += ' {}ch {:f} {:f}'.format(c, (float)(data_K[i]), (float)(data_S[i])) ;
            except Exception as e:
                print('Warning!! Invalid data obtained (error: {})! --> -1 filled'.format(e))
                line += ' {}ch -1 -1'.format(c) ;
                pass
            pass;
        f.write(line+'\n');
        f.flush();
        if isTest : break;
        sleep(dt);
        pass; # end of while loop
 
    pass;
