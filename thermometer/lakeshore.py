#!/usr/bin/env python

import serial
import socket
import numpy as np;
from time import sleep

class LakeshoreError(Exception):
    def __init__(self, message):
        self.msg = "LakeshoreError: " + str(message)
        pass
    def __str__(self):
        return self.msg
    pass

class Lakeshore(object):
    def __init__(self, devfile, TIMEOUT_IGNORE = True):
        ## devfile: device file name
        # RS232C connection
        if isinstance(devfile, str) :
            self.devtype = 'serial';
            self.dev = serial.Serial(devfile,
                         9600,
                         timeout=0.0001,
                         parity=serial.PARITY_ODD,
                         bytesize=7)
        elif isinstance(devfile, dict) :
            self.devtype = 'ethernet';
            self.dev = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if not( devfile.has_key('ip') and devfile.has_key('mask') and devfile.has_key('port') ) :
                raise LakeshoreError('dictionary keys error in arguments {}'.format(','.join(devfile.keys())));
                pass;
            self.dev.connect((devfile['ip'], devfile['port']));
        else :
            raise LakeshoreError('argument error');
            pass;
        if self.dev == None: raise LakeshoreError("open error")
        self.TIMEOUT_IGNORE = TIMEOUT_IGNORE
        self.chs = []
        pass

    def __del__(self):
        self.dev.close()
        del self
        pass

    def write(self, command):
        if self.devtype=='serial'   : 
            self.dev.write((command + '\n').encode())
            sleep(0.1)
        elif self.devtype=='ethernet' : 
            self.dev.send((command + '\n').encode())
            pass;
        pass

    def read(self):
        ret = ""
        if self.devtype=='serial' :
            for i in range(10000): ## timeout > 0.0001 sec * 10000
                ret += self.dev.readline().decode()
                if len(ret) > 0 and ret[-1] == '\n': break
                pass
            if len(ret) == 0 or ret[-1] != '\n':
                if not self.TIMEOUT_IGNORE:
                    raise LakeshoreError("read error: time out")
                pass
        elif self.devtype=='ethernet' : 
            ret = self.dev.recv(4096)
            pass;
        return ret.strip()

    def readclear(self):
        ret = ""
        if self.devtype=='serial' :
            ret += self.dev.readline().decode()
            while len(ret) > 0 and ret[-1] != '\n': ret += self.dev.readline().decode()
        elif self.devtype=='ethernet' : 
            # Nothing to do
            pass;
        return
    def getonoff(self, ch=1):
        if ch>0 :
            self.readclear()
            if self.devtype=='serial' :
                self.write('input? %d' %ch)
                ret = self.read().split(',')[0]
                ret = (ret=='1');
            elif self.devtype=='ethernet' : 
                self.write('intype? %d' %ch)
                #ret  = self.read();
                #ret = self.read().split(',')[0]
                ret = self.read().split(',')[0] ;
                ret = (len(ret)>0) ;
                pass;
        else : 
            return True;
        return ret;

    def gettemp(self, ch = 1, mode = "K"):
        ## ch: 1, 2, ...
        ## mode: S: sensor unit, K: kelvin, R: resistance for LS372
        onoff = self.getonoff(ch);
        self.readclear()
        if mode == "S":
            self.write('srdg? %d' %ch)
        elif mode == "K":
            self.write('krdg? %d' %ch)
        elif mode == "R":
            self.write('rdgr? %d' %ch)
        else:
            raise LakeshoreError("gettemp: mode error")
        ret = self.read();
        return ret if onoff else 0;

    def gettemps(self, chlist = None, mode = "K"):
        ## chlist: channel list (e.g. ['a', 'b', 'c', 'd'])
        if chlist != None: self.chs = chlist
        ret = []
        for c in self.chs: ret.append(self.gettemp(c, mode))
        return ret

    def relay(self, ch, ON = False):
        if int(ch) < 1 or int(ch) > 8:
            raise LakeshoreError("relay: channel is 1-8")
        sw = "0"
        if ON: sw = "1"
        while self.relaystatech(ch) != ON:
            self.write('relay ' + str(ch) + ' ' + sw)
        return

    def relaystate(self):
        self.readclear()
        self.write('relayst?')
        try:
            return int(self.read())
        except:
            return 0

    def relaystatech(self, ch):
        c = int(ch)
        if ch < 1 or ch > 8:
            raise LakeshoreError("relay: channel is 1-8")
        st = self.relaystate()
        val = 1
        for i in range(1, c): val *= 2
        if st & val == 0: return False
        return True

    def modifyDigit(self, value, Ndigit) :
        value_str = '';
        if value>=np.power(10,Ndigit-1) : value_str = '{:d}'.format(value);
        else :
            for i in range(Ndigit-2,-1,-1) :
                if value>=np.power(10,i) : 
                    format_str = '{{:.{}f}}'.format(Ndigit-i-1);
                    value_str  = format_str.format(value);
                    break;
                pass;
            pass;
        # case of value<1.
        if value_str=='' : 
            format_str = '{{:.{}f}}'.format(Ndigit-1);
            value_str = format_str.format(value);
            pass;
        return value_str;

    # name         : <=15 character
    # serialnumber : <=10 character
    # dataformat   : 3=ohm/K (linear), 4=log(ohm)/K(linear), 7=ohm/K (cubic spline)
    # posneg : negative(1) or positive(2) for the coefficient
    def addcalibration(self, ch, name='aho', serialnumber=' ', dataformat=0, templimit=330, posneg=1):
        modtemplimit = self.modifyDigit(templimit, 6);
        if self.devtype=='serial'   : 
            command = 'CRVHDR 2{},{},{},{},{},{}'.format(ch,name,serialnumber,dataformat,modtemplimit,posneg);
            print(command)
            self.write(command)
            sleep(0.2)
        elif self.devtype=='ethernet' : 
            command = 'CRVHDR 2{},"{}","{}",{},{},{}'.format(ch,name,serialnumber,dataformat,modtemplimit,posneg);
            print(command);
            self.write(command)
            pass;
        return True

    def deletecalibration(self, ch):
        if self.devtype=='serial'   : 
            command = 'CRVDEL 2{}'.format(ch);
            self.write(command)
            sleep(0.1)
        elif self.devtype=='ethernet' : 
            command = 'CRVDEL 2{}'.format(ch);
            print(command);
            self.write(command)
            pass;
        return True

    def checkcalibration(self, ch):
        if self.devtype=='serial'   : 
            command = 'CRVHDR? 2{}'.format(ch);
            self.write(command)
            sleep(0.1)
            ret = self.read();
        elif self.devtype=='ethernet' : 
            command = 'CRVHDR? 2{}'.format(ch);
            self.write(command)
            ret = self.read();
            pass;
        return ret;

    def setcalibration(self, ch, temp, value, i=0):
        modvalue = self.modifyDigit(value,6);
        modtemp  = self.modifyDigit(temp ,6);
        if self.devtype=='serial'   : 
            command = 'CRVPT 2{},{},{},{}'.format(ch,i+1,modvalue,modtemp);
            print(command)
            self.write(command)
            sleep(0.1)
        elif self.devtype=='ethernet' : 
            command = 'CRVPT 2{},{},{},{}'.format(ch,i+1,modvalue,modtemp);
            self.write(command)
            pass;
        return True

    def getcalibration(self, ch, i=0, doPrint=False):
        values = 0;
        if self.devtype=='serial'   : 
            command = 'CRVPT? 2{},{}'.format(ch,i+1);
            self.write(command)
            sleep(0.1)
            ret = self.read()
        elif self.devtype=='ethernet' : 
            command = 'CRVPT? 2{},{}'.format(ch,i+1)
            self.write(command)
            ret = self.read()
            print( 'curve=2{}, i={} : {}'.format(ch, i+1, ret) );
            pass;
        return values;

    def printcalibration(self, c, imax=201, doPrint=False):
        ret = self.checkcalibration(c);
        if doPrint : print( 'curve status: {}'.format(ret) );
        for i in range(0,imax,10):
            self.getcalibration(c, i, doPrint);
            pass;
        return;

    def changecalibrationcurve(self, ch=1, n=1):
        if self.devtype=='serial'   : 
            command = 'INCRV {},{}'.format(ch,n);
            self.write(command)
            sleep(0.1)
        elif self.devtype=='ethernet' : 
            command = 'INCRV {},{}'.format(ch,n);
            self.write(command)
            pass;
        return True;

    def getcalibrationcurve(self, ch=1, doPrint=False):
        if self.devtype=='serial'   : 
            command = 'INCRV? {}'.format(ch);
            self.write(command)
            sleep(0.1)
            ret = self.read();
        elif self.devtype=='ethernet' : 
            command = 'INCRV? {}'.format(ch);
            self.write(command)
            ret = self.read();
            pass;
        if doPrint : 
            print( 'getcalibrationcurve(): channel={} : {}'.format(ch,ret) );
            pass
        return True;

    # sample heater

    # sample heater output ratio of max current
    def getsampleheaterratio(self):
        self.readclear()
        self.write('htr?')
        return (float)(self.read())*0.01; 
    # sample heater output max current
    def getsampleheatermax(self):
        self.readclear()
        self.write('range?')
        intToAmpere = [0., 31.6e-6, 100.e-6, 316.e-6, 1.0e-3, 3.16e-3, 10.0e-3, 31.6e-3, 100.e-3] ;
        ret = self.read();
        return intToAmpere[ (int)(ret) ];  
    # sample heater output current
    def getsampleheater(self):
        ratio      = self.getsampleheaterratio();
        maxcurrent = self.getsampleheatermax();
        return ratio * maxcurrent ;

    pass # End of class Lakeshore


if __name__ == '__main__':
    cc = Lakeshore('/dev/ttyUSB0')
    data = cc.gettemps([1, 2, 3, 4, 6, 7, 8], "S")
    print(data)
    pass
