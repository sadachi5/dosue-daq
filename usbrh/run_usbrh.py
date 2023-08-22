import os
import datetime
import time
from subprocess import check_output

outdirectory = '/data/usbrh'

def main(dt=10):
    start = datetime.datetime.now();
    f = None

    def openfile(filename):
        try:
            f = open(filename, "a")
        except:
            print( 'Error!! Couldn\'t open file {}'.format(filename) );
            exit(1)
            pass;
        return f
 
    while True :

        now  = datetime.datetime.now();
        nowStr = now.strftime('%Y-%m-%d');
        outputfilename = '{}/data_{}.dat'.format( outdirectory, nowStr );

        if (now.day) != (start.day) :
            if f is not None: 
                f.close()
                del f
                f = None
                pass
            pass
            
        # Open a new file
        #print(f)
        if f is None:
            print('Open new file')
            f = openfile(outputfilename)
            openStr = now.strftime('%Y/%m/%d %H:%M:%S (Unix time)');
            line   = '# unix-time {} '.format(openStr);
            line += ' Temp[deg] Humy[perc]';
            f.write(line+'\n');
            f.flush();
            pass

        # Get temperature & humidity
        data = check_output(['/usr/local/bin/usbrh']).decode().split(' ')
        temp = data[0]
        humid = data[1][:-1]

        # Output line
        line = ''
        line += '{}'.format(int(now.timestamp()))
        line += ' '
        line += now.strftime('%Y/%m/%d %H:%M:%S')
        try: 
            line += ' {:f} {:f}'.format((float)(temp), (float)(humid))
        except Exception as e:
            print('Warning!! Invalid data obtained (error: {})! --> -1 filled'.format(e))
            line += ' -1 -1'
            pass

        # Write line
        f.write(line+'\n');
        f.flush();

        # Time interval
        time.sleep(dt);
        pass; # end of while loop

    return True

if __name__=='__main__':
    main()
