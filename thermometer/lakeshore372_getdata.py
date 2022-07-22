#!/bin/env python
import os, sys;
import serial;
import lakeshore;
from time import sleep;
import datetime;
       
isTest = False;
#isTest = True;


if __name__ == '__main__':

    devlocation  = '169.254.235.124,255.255.0.0,7777';
    dt = 60
    channels = [-1,1]; # -1 : sample heater, -2 : warmup heater
 
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
                if   c>0   : line += ' {}ch <Temp[K]> <Raw value>'.format(c);
                elif c==-1 : line += ' sample-heater <current[A]>';
                elif c==-2 : line += ' warmup-heater <current[A]>';
                pass;
            f.write(line+'\n');
            f.flush();
            pass;
        if(len(sys.argv) > 2): devlocation = sys.argv[2];
        if(len(sys.argv) > 3): dt          = int(sys.argv[3])
    except:
        print( 'Error!! Arguments were :');
        print( sys.argv );
        print( 'Error!! Usage: python lakeshore372_getdata.py <output file> [<device location=\'ip,subnetmask,port\'> [<interval(sec) = 60>]]' );
        exit(1)
        pass
 
    devTmp = devlocation.split(',');
    if len(devTmp)>2 :
        devlocationDict = {'ip':devTmp[0], 'mask':devTmp[1], 'port':(int)(devTmp[2]) };
    else :
        print( 'Error!! device location is not suitable! {}'.format(devlocation) );
        print( '        It should be \'XXXX(ip),YYYY(subnetmask),ZZZZ(port)\'' );
        exit(1)
        pass;
    ls = lakeshore.Lakeshore(devlocationDict);
 
    while True :
 
        now  = datetime.datetime.now();
        ## if AM/PM is different between now and start, the job is finished to change the output file.
        #if (now.hour>=12) != (start.hour>=12) : break; 
        if (now.day) != (start.day) : break; 
       
        channelsSensor = [ c for c in channels if c>0 ];
        if isTest : print( 'channelsSensor', channelsSensor );
        if len(channelsSensor) > 0 :
            data_K = ls.gettemps(channelsSensor, "K")
            data_S = ls.gettemps(channelsSensor, "R")
        data_Sheater = ls.getsampleheater();
        for i, c in enumerate(channels) :
            if c==-1 or c==-2 :
                data_K.insert(i, c);
                data_S.insert(i, c);
                pass;
            pass;
        line = '';
       
        if isTest :
            print(  'data_K      ', data_K);
            print(  'data_S      ', data_S);
            print(  'data_Sheater', data_Sheater);
            pass;
       
        line += '{}'.format(int(now.timestamp()));
        line += ' ';
        line += now.strftime('%Y/%m/%d %H:%M:%S');
        for i, c in enumerate(channels) :
            if   c>0:
                try: 
                    line += ' {}ch {:f} {:f}'.format(c, (float)(data_K[i]), (float)(data_S[i])) ;
                except Exception as e:
                    print('Warning!! Invalid data obtained (error: {})! --> -1 filled'.format(e))
                    line += ' {}ch -1 -1'.format(c) ;
            elif c==-1 : line += ' sample-heater {:.3e}'.format(data_Sheater);
            elif c==-2 : line += ' warmup-heater {:.3e}'.format(0);
            pass;
        f.write(line+'\n');
        f.flush();
        if isTest : break;
        sleep(dt);
        pass; # end of while
 
    pass;
