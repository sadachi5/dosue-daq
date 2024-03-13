#!/bin/env python
import os, sys
import serial
from time import sleep
import binascii
import struct

devlocation = '/dev/ttyUSB2'

BANDRATE   = 9600 # for CC-10 # 9600 is best BANDRATE. With the others perhaps you cannot get response from CC-10.
#BANDRATE   = 4800 # for CC-10
#BANDRATE   = 1200 # for CC-10
TIMEOUT    = 0    
MAXREADLOOP= 100000 # max. loop in read()
SSLEEP   = sleep(0.1)
CHANNEL  = 0
MINSIZE = 1
 

ser = serial.Serial(devlocation, 
   baudrate =BANDRATE, 
   timeout  =TIMEOUT, 
   bytesize =serial.EIGHTBITS, 
   parity   =serial.PARITY_NONE, 
   stopbits =serial.STOPBITS_ONE, 
   )

ser.reset_input_buffer()
ser.reset_output_buffer()

def read(ser, minsize=MINSIZE):
    read_list = []
    for m in range(MAXREADLOOP) :
        read0 = ser.readline()
        #print('1:', read0)
        read0 = read0.decode()
        #print('2:', read0)
        size0 = len(read0)

        if size0>0 : 
            print( 'read0 = {}'.format(repr(read0)) )
            read_list += read0 if len(read_list)>0 else read0.lstrip('\x00') 
            print( 'read  = {}'.format(repr(read_list)) )
            pass

        # Exit inner loop and proceed
        if len(read_list) >= minsize : break
        pass

    return read_list

def write(ser, command):
  print( 'Write : {}'.format(repr(command)) )
  ser.write(command.encode())
  return

write(ser, 'AYT\r')
_read = read(ser, 3)
print(f'"{_read}"')
write(ser, '\x05')
_read = read(ser, 40)
_read_str = ''.join(_read)
print(f'"{_read_str}"')

ser.close()
