#!/usr/bin/env python
import socket
import numpy as np
from time import sleep
import time
import matplotlib.pyplot as plt
import os, sys
import datetime

IP_ADDRESS = '192.168.215.247'
PORT = 49153

def write(soc,word:str):
    word += '\r\n'
    soc.send(word.encode())
    return 0;

def read(soc):
    ret_msg = ''
    i=0
    while True:
        print(f'i={i}')
        try:
            print('0');
            rcvmsg = soc.recv(1024).decode()
        except Exception as e:
            print(f'Error! {e}')
            soc.close()
            return None
        print('1');
        ret_msg += rcvmsg
        if rcvmsg[-1] == '\n':
            break        
        print('2');
        i=i+1
        pass
    print(f'read = {ret_msg}');
    return ret_msg.strip()

def writeread(soc, word):
    print(f'writeread: {word}');
    write(soc, word)
    ret = read(soc)
    if ret is None :
        print('Error! Failed to read!')
        print('       --> Exit()')
        sys.exit(1)
        pass
    return ret;

def read_data(soc):
    ut = time.time()
    rawstr = writeread(soc, 'READ:SAN?');
    if rawstr is None : return None;
    data = np.array([float(ns) for ns in rawstr.split(',')])
    return data[::2], data[1::2], ut


def reboot(run=False) :
    print('socket')
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    print('connect')
    soc.connect((IP_ADDRESS, PORT))
    print('settimeout')
    soc.settimeout(10)

    # Reboot
    print(f'run = {run}');
    if run: 
        print('Rebooting!!');
        write(soc, 'SYST:REB');
        pass

    soc.close();
    return 0;


if __name__=='__main__':
    run=False
    print(sys.argv)
    if len(sys.argv)>1:
        run = bool(int(sys.argv[1]))
        pass
    reboot(run);
    pass;
