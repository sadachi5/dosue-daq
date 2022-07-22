#!/bin/env python
import os, sys;
import serial;
from time import sleep;
import binascii;
import struct;



###############################
# Vaccum Sensor CC-10 via USB #
###############################

class VacuumSensorCC10Error(Exception) :
  def __init__(self, message):
    self.msg = "VacuumSensorCC10Error: " + str(message)
    pass
  def __str__(self):
    return self.msg
  pass

class VacuumSensorCC10(object):
  def __init__(self, devlocation, verbose=0) :
    #self.BANDRATE = 38400; # for CC-10
    #self.BANDRATE   = 19200; # for CC-10
    self.BANDRATE   = 9600; # for CC-10 # 9600 is best BANDRATE. With the others perhaps you cannot get response from CC-10.
    #self.BANDRATE   = 4800; # for CC-10
    #self.BANDRATE   = 1200; # for CC-10
    self.TIMEOUT    = 0    ;
    self.MAXREADLOOP= 100000; # max. loop in read()
    self.SSLEEP   = sleep(0.1);
    self.CHANNEL  = 0;
    self.minsize = {
        'R':[0,8,12,12,12,8],
        'W':[0,4,4,4,4,4],
        'C':[0,8,8],
        'S':[0,8,8,8,8,8,8,8,8,8],
        'E':[8],
        };
    self.devlocation = devlocation;
    self.verbose     = verbose    ;
    self.ser = serial.Serial(self.devlocation, 
            baudrate =self.BANDRATE, 
            timeout  =self.TIMEOUT, 
            bytesize =serial.EIGHTBITS, 
            parity   =serial.PARITY_EVEN, 
            stopbits =serial.STOPBITS_ONE, 
            );
    if self.verbose > 0 :
      print('devlocation = {}'.format(self.devlocation));
      print('verbose     = {}'.format(self.verbose    ));
      print('bandrate    = {}'.format(self.BANDRATE   ));
      print('timeout     = {}'.format(self.TIMEOUT    ));
      print('minsize     = {}'.format(self.minsize    ));
      pass;
        
    self.ser.reset_input_buffer();
    self.ser.reset_output_buffer();

    pass;

  def __del__(self):
    self.ser.close()
    del self
    pass
  
  # No longer used
  def wait(self):
    #while True : 
    #  if self.ser.inWaiting > 0 : break  ;
    #  pass;
    pass;

  def write(self, command):
    if self.verbose>0 : print( 'Write : {}'.format(repr(command)) );
    self.ser.write(command.encode());
    return;

  def read(self,C,M):
    read = [];
    self.wait();

    if self.verbose>0 : print('Read');
    for m in range(self.MAXREADLOOP) :

      if self.verbose>2 : print('readline()');
      read0 = self.ser.readline().decode();
      size0 = len(read0);

      if size0>0 : 
        if self.verbose>1 : print( 'read0 = {}'.format(repr(read0)) );
        read += read0 if len(read)>0 else read0.lstrip('\x00') ;
        if self.verbose>1 : print( 'read  = {}'.format(repr(read)) );
        pass;

      # Exit inner loop and proceed
      if len(read) >= self.minsize[C][M] : break;

      pass;

    if len(read)<self.minsize[C][M] :
      print( 'Error!! Could not read from CC-10 vacuum sensor correctly!' );
      print( '        COMMAND = {}'.format(C)    );
      print( '        MODE    = {}'.format(M)    );
      print( '        read    = {}'.format(read) );
      print( '        Returning blank... ("")'   );
      return "";
    
    return read;

  def checkStatus(self) :
    self.ser.reset_input_buffer();
    self.ser.reset_output_buffer();
    C = 'S'; # COMMAND
    M =  2 ; # MODE
    command="\x02{}{}{}\x0d".format(self.CHANNEL,C,M);
    self.write(command);
    ret = self.read(C,M);
    status = 0 if len(ret)<8 else (int)(ret[6]) ;

    return status; # 0: Error, 1:Measure

  def getError(self) :
    self.ser.reset_input_buffer();
    self.ser.reset_output_buffer();
    C = 'S'; # COMMAND
    M =  5 ; # MODE
    command="\x02{}{}{}\x0d".format(self.CHANNEL,C,M);
    self.write(command);
    ret = self.read(C,M);
    if len(ret)<8 :
      print( 'Error!! Could not get error message! The size of return < 8 ({})'.format(len(ret)) );
      print( '        return = {}'.format(ret) );
      sys.exit(1);
      pass;
    error = [ (bool)(c) for c in ret[3:7] ];
    message = "";
    if error[0] : message += "Erro "     ;
    if error[1] : message += "AdEr "     ;
    if error[2] : message += "CALE "     ;
    if error[3] : message += "EE-Error " ;
    return message;
   

  def readVacuum(self) :

    # check status
    #if self.checkStatus()!=1 :
    #  print( 'Error!! The status of vacuum sensor CC-10 has error!!' );
    #  errorMessage = self.getError();
    #  print( '        Error Status = "{}"'.format(errorMessage) );
    #  print( '        Return -1' );
    #  return -1;

    # write command to read vacuum pressure
    self.ser.reset_input_buffer();
    self.ser.reset_output_buffer();
    C = 'S'; # COMMAND
    M =  1 ; # MODE
    command="\x02{}{}{}\x0d".format(self.CHANNEL,C,M);
    self.write(command);

    # read
    ret = self.read(C,M);
    if len(ret)<8 :
      print( 'Error!! Could not get error message! The size of return < 8 ({})'.format(len(ret)) );
      print( '        return = {}'.format(ret) );
      print( '        Return -1' );
      return -1;
    if self.verbose>0 : print( 'return   = {}'.format(ret) );
    pp = (float)( '{}.{}'.format(ret[3],ret[4]) ) ;
    s  = +1. if ret[5]=='1' else -1. ;
    e  = (float)(ret[6]);
    pressure = pp * pow(10, s*e);
    if self.verbose>0 : print( 'pressure = {}'.format(pressure) );
    
    return pressure;
  



###################################
# Vaccum Sensor TPG361-10 via USB #
###################################

class VacuumSensorTPG361Error(Exception) :
  def __init__(self, message):
    self.msg = "VacuumSensorTPG361Error: " + str(message)
    pass
  def __str__(self):
    return self.msg
  pass

class VacuumSensorTPG361(object):
  def __init__(self, devlocation, verbose=0) :
    self.BANDRATE   = 9600; 
    self.TIMEOUT    = 0    ;
    self.MAXREADLOOP= 100000; # max. loop in read()
    self.SSLEEP   = sleep(0.1);
    self.CHANNEL  = 0;
    self.COMMANDS = {
        'PR1\r':{'minsize':15, 'receive':'\x06\r\n', 'transmit':'\x05'},
        'PR2\r':{'minsize':15, 'receive':'\x06\r\n', 'transmit':'\x05'},
        'ERR\r':{'minsize': 6, 'receive':'\x06\r\n', 'transmit':'\x05'},
        };
    self.devlocation = devlocation;
    self.verbose     = verbose    ;
    self.ser = serial.Serial(self.devlocation, 
            baudrate =self.BANDRATE, 
            timeout  =self.TIMEOUT, 
            bytesize =serial.EIGHTBITS, 
            parity   =serial.PARITY_NONE, 
            stopbits =serial.STOPBITS_ONE, 
            );
    if self.verbose > 0 :
      print('devlocation = {}'.format(self.devlocation));
      print('verbose     = {}'.format(self.verbose    ));
      print('bandrate    = {}'.format(self.BANDRATE   ));
      print('timeout     = {}'.format(self.TIMEOUT    ));
      print('commands    = {}'.format(self.COMMANDS   ));
      pass;
        
    self.ser.reset_input_buffer();
    self.ser.reset_output_buffer();

    pass;

  def __del__(self):
    self.ser.close()
    del self
    pass
  
  def wait(self):
    while True : 
      if self.ser.inWaiting > 0 : break  ;
      pass;
    pass;

  def write(self, command):
    if self.verbose>0 : print( 'Write : {}'.format(repr(command)) );
    self.ser.write(command.encode());
    return;

  def read(self,minsize):
    read = [];
    self.wait();

    if self.verbose>0 : print('Read');
    for m in range(self.MAXREADLOOP) :

      if self.verbose>2 : print('readline()');
      read0 = self.ser.readline().decode();
      size0 = len(read0);

      if size0>0 : 
        if self.verbose>1 : print( 'read0 = {}'.format(repr(read0)) );
        read += read0 if len(read)>0 else read0.lstrip('\x00') ;
        if self.verbose>1 : print( 'read  = {}'.format(repr(read)) );
        pass;

      # Exit inner loop and proceed
      if len(read) >= minsize : break;

      pass;

    return read;

  def command(self, command) :
    self.ser.reset_input_buffer();
    self.ser.reset_output_buffer();
    receive  = self.COMMANDS[command]['receive'];
    transmit = self.COMMANDS[command]['transmit'];
    minsize  = self.COMMANDS[command]['minsize'];

    self.write(command);
    received = self.read(len(receive));
    if received != [ r for r in receive ]:
      print( 'WARNING!! Could not read from TPG-361 vacuum sensor! (Receive failed)' );
      print( '        COMMAND        = {}'.format(command ) );
      print( '        To be received = {}'.format(receive ) );
      print( '        Received       = {}'.format(received) );
      pass;

    self.write(transmit);
    read = self.read(minsize);
    if len(read) < minsize :
      print( 'ERROR!! Could not read from TPG-361 vacuum sensor! (Read failed)' );
      print( '        COMMAND     = {}'.format(command  ) );
      print( '        minsize     = {}'.format(minsize  ) );
      print( '        readsize    = {}'.format(len(read)) );
      print( '        read        = {}'.format(read     ) );
      print( '        Returning blank... ("")'   );
      return "";
      pass;

    return read;

  def getError(self) :
    self.ser.reset_input_buffer();
    self.ser.reset_output_buffer();
    command = 'ERR\r'; # COMMAND
    ret = self.command(command);
    message = "";
    if ret=="" : 
      print( 'ERROR!! Could not read error status from TPG-361 vacuum sensor!' );
      print( '        return = {}'.format(ret) );
      return 'ReadError ';
      
    error = [ (bool)(int(c)) for c in ret[:4] ]; # remove \r or \n
    if error[0] : message += "ControllerError " ;
    if error[1] : message += "NoHardware "      ;
    if error[2] : message += "ParameterError "  ;
    if error[3] : message += "SytaxError "      ;
    return message;
   

  def readVacuum(self) :

    # check status
    errorMessage = self.getError();
    if errorMessage!="":
      print( 'Error!! The status of vacuum sensor TPG-361 has error!!' );
      print( '        Error Status = "{}"'.format(errorMessage) );
      print( '        Return -1' );
      return -1;

    # write command to read vacuum pressure
    self.ser.reset_input_buffer();
    self.ser.reset_output_buffer();
    command = 'PR1\r'; # COMMAND
    ret = self.command(command);

    if self.verbose>0 : print( 'return   = {}'.format(ret) );
    pressure = (float)(''.join(ret[2:13]));
    if self.verbose>0 : print( 'pressure = {} Pa'.format(pressure) );
    
    return pressure;
  
