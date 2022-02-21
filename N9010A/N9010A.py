
#!/usr/bin/env python
import socket
import numpy as np
from time import sleep
import time
import matplotlib.pyplot as plt
import os
import datetime
import pathlib
import argparse
import struct


IP_ADDRESS = '192.168.215.113'
PORT = 5025
outt = 300
DATA_FORMAT='REAL,64' # 'REAL,64'

class spa_data:
    def __init__(self, freq, powDBm, MesTimePoint):
        self._freq = np.array(freq)
        self._powDBm = np.array(powDBm)
        self._time = MesTimePoint

    @property
    def powDBm(self):
        return self._powDBm

    @property
    def amp(self):
        return np.power(10., self._powDBm/10.)/1000.

    @property
    def freq(self):
        return self._freq

    @property
    def time(self):
        return self._time


class N9010A:
    # sweep_mode = 'SWEEP' or 'FFT'
    def __init__(self, host_ip=IP_ADDRESS, port=PORT, sweep_mode='SWEEP'):
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host_ip = host_ip
        self._port = port
        self._connected = False
        self._outtime = outt
        self._sweep_mode = sweep_mode

    def __del__(self):
        if self._connected:
            self.close()
        
    def _w(self, word:str):
        word += '\r\n'
        self._soc.send(word.encode())

    def _r(self, decode=True):
        if decode:
            ret_msg = ''
            end = '\n'
        else:
            ret_msg = b''
            end = b'\n'
            pass
        self._soc.settimeout(self.outtime)
        while True:
            rcvmsg = self._soc.recv(1024)
            if decode:
                rcvmsg = rcvmsg.decode()
                pass
            ret_msg += rcvmsg
            if rcvmsg[-1:] == end:
                break        
        return ret_msg.strip()

    def _wr(self, word, decode=True):
        self._w(word)
        return self._r(decode=decode) 

    def connect(self):
        if self._connected:
            raise Exception("Already connected.")
        self._soc.connect((self._host_ip, self._port))
        self._w('*CLS')
        self._w('*RST')
        self._w('*WAI')
        self._w('INIT:CONT OFF')
        self._w('INIT:SAN')
        if self._sweep_mode == 'SWEEP':
            self._w('SWE:TYPE SWE')
        elif self._sweep_mode == 'FFT':
            self._w('SWE:TYPE FFT')
        else:
            print('N9010A:connect(): ERROR! There is no sweep mode of "{self._sweep_type}"!')
            print('N9010A:connect(): ERROR! sweep mode is only "SWEEP" or "FFT".')
        self._w(f'FORM {DATA_FORMAT}') # 32bit binary (float)
        if DATA_FORMAT == 'REAL,32':
            binary_size = 8
            binary_format = 'f'
        elif DATA_FORMAT == 'REAL,64':
            binary_size = 16
            binary_format = 'd'
        else:
            print('N9010A:connect(): ERROR! There is no data format of "{DATA_FORMAT}"!')
            pass
        self._soc.settimeout(10)

    def close(self):
        if self._connected:
            self._soc.close()
            self._connected = False

    def decode_data(self, rawbin, verbose=0):
        nchar = (int)(rawbin[1:2].decode())
        if verbose>1: print(f'N9010A:decode_data(): nchar = {nchar}')
        nbinary = (int)((int)(rawbin[2:2+nchar].decode())/8)
        if DATA_FORMAT == 'REAL,32':
            unpack_format = '>'+'f'*nbinary
        elif DATA_FORMAT == 'REAL,64':
            unpack_format = '>'+'d'*nbinary
        else:
            print('N9010A:decode_data(): ERROR! There is no data format of "{DATA_FORMAT}"!')
            pass
        data = struct.unpack(unpack_format, rawbin[2+nchar:])
        if verbose>1: 
            print(f'N9010A:decode_data(): nbinary = {nbinary}')
            print(f'N9010A:decode_data(): binary data length = {len(rawbin[2+nchar:])}')
            print(f'N9010A:decode_data(): unpack format = {unpack_format}')
            print(f'N9010A:decode_data(): data = {data}')
            pass
        return data

    def read_data(self) -> spa_data:
        ut = time.time()
        rawstr = self._wr('READ:SAN?', decode=False)
        rawstr = self.decode_data(rawstr)
        data = np.array([float(ns) for ns in rawstr])
        return spa_data(data[::2], data[1::2], ut)

    def cps_on(self):
        return self._w('CALC:MARK:CPS ON')

    def cps_off(self):
        return self._w('CALC:MARK:CPS OFF')

    def cal_marker_y(self):
        return self._wr('CALC:MARK:Y?')

    def cal_marker_x(self):
        return self._wr('CALC:MARK:X?')

#    def cal_marker_max(self):
#        return self._wr(':CALCulate:MARKer{1}:MAXimum')

    @property
    def outtime(self):
        return self._outtime

    @outtime.setter
    def outtime(self, outtime):
        self._outtime = outtime
        
    @property
    def time(self) -> float:
        return float(self._wr('SWE:TIME?'))

    @time.setter
    def time(self, time_sec:float):
        return self._w(f'SWE:TIME {time_sec}')

    @property
    def freq_start(self) -> float:
        return float(self._wr('FREQ:STAR?'))

    @freq_start.setter
    def freq_start(self, freq_GHz:float):
        self._w(f'FREQ:STAR {freq_GHz} GHz')

    @property
    def freq_stop(self) -> float:
        return float(self._wr('FREQ:STOP?'))

    @freq_stop.setter
    def freq_stop(self, freq_GHz:float):
        self._w(f'FREQ:STOP {freq_GHz} GHz')

    @property
    def band_wid(self) -> float:
        return float(self._wr('BWID:RES?'))

    @band_wid.setter
    def band_wid(self, wid_MHz:float):
        self._w(f'BWID:RES {wid_MHz} MHz')

    @property
    def aver_coun(self) -> int:
        return int(self._wr('AVER:COUN?'))

    @aver_coun.setter
    def aver_coun(self,count:int):
        self._w(f'AVER:COUN {count}')

    @property
    def is_continuous(self) -> bool:
        b = int(self._wr('INIT:CONT?:'))
        return b == 1

    @is_continuous.setter
    def is_continuous(self, cont:bool):
        self._w(f'INIT:CONT {"1" if cont else "0"}')

    @property
    def band_rat(self) -> float:
        return float(self._wr('FREQ:SPAN:BAND:RAT?'))

    @band_rat.setter
    def band_rat(self, br:float):
        self._w(f'FREQ:SPAN:BAND:RAT {br}')
                
    @property
    def band(self) -> float:
        return float(self._wr('BAND?'))
    
    @band.setter
    def band(self, b_Hz:float):
        if b_Hz < 1e3:
            self._w(f'BAND {b_Hz} Hz')
        elif b_Hz < 1e6:
            self._w(f'BAND {b_Hz/1e3} KHz')
        elif b_Hz < 1e9:
            self._w(f'BAND {b_Hz/1e6} MHz')

    @property
    def npoints(self) -> int:
        return int(self._wr('SWE:POIN?'))

    @npoints.setter
    def npoints(self, n:int):
        self._w(f'SWE:POIN {n}')

    @property
    def det_mode(self) -> str:
        # NORMal, AVERage, POSitive, SAMPle, NEGative, QPEak, EAVerage, RAVerage
        return str(self._wr('DET?'))

    @det_mode.setter
    def det_mode(self, mode:str):
        #self._w(f'TRAC:TYPE {mode}')
        self._w(f'DET {mode}')
 
    
def main(outdir='~/data/n9010a', 
         mode = 'SWEEP',
         start = 19.999995, #GHz
         stop = 20.000005, #GHz
         rbw = 300, # Hz
         npoints = 0, # points
         nAve = 1, # counts
         overwrite = False, # do overwrite or not
         ip_address = IP_ADDRESS,
         filename=None):
    spa = N9010A(host_ip = ip_address, sweep_mode = mode)
    spa.connect()

    spa.freq_start = start #GHz
    print(f'Start freq: {spa.freq_start} GHz')
    spa.freq_stop = stop #GHz
    print(f'Stop freq : {spa.freq_stop} GHz')
    spa.npoints = npoints #points
    print(f'npoints : {spa.npoints}')
    spa.band = rbw #Hz
    print(f'Band Width : {spa.band} Hz')
    
    print(f'Sweep Time : {spa.time} s')
    
    spa.aver_coun = nAve
    print(f'Average Count : {spa.aver_coun}')

    spa.det_mode = 'AVERage'
    #spa.det_mode = 'NORM'
    print(f'Detection Mode : {spa.det_mode}')

    
    start_time = time.time()
    result = spa.read_data()
    stop_time = time.time()
    print(f'Elapsed time for read_data() = {stop_time-start_time} sec')
    fig, ax = plt.subplots()
    ax.plot(result.freq/1.e9, result.powDBm)
    ax.set_xlabel('Freq [GHz]')
    ax.set_ylabel('dBm')
    ax.grid()
    fig.tight_layout()

    # make output folder                                                     
    outdir = pathlib.Path(outdir).expanduser() # convert '~/' directory to full path name
    if not os.path.exists(f'{outdir}'):
        os.mkdir(f'{outdir}')
        pass
    # make today's folder                                                     
    today = str(datetime.datetime.now().date())
    todaydir = f'{outdir}/{today}'
    if not os.path.exists(todaydir):
        os.mkdir(f'{todaydir}')
        os.mkdir(f'{todaydir}/data')
        os.mkdir(f'{todaydir}/figure')
        pass

    # make new file                                                           
    if filename is None:
        filename = input("filename ? : ")
        pass
    fpath = "data/" + today + "/data/" + filename + ".dat"
    if filename=='':
        print(f'Do NOT save the data!')
        ms.close()
        plt.close()
        print('End')
        return 0
    fdatapath = f'{todaydir}/data/{filename}.dat'
    if os.path.exists(fdatapath):
        if overwrite: _filename = filename;
        else        : _filename = input("other : ")
        if _filename == filename: print(f'Warning! The output file ({filename}.dat) is overwriten!')
        filename = _filename
        fdatapath = f'{todaydir}/data/{filename}.dat'
        pass
    #fconfigpath = f'{todaydir}/data/{filename}.csv'
    ffigpath = f'{todaydir}/figure/{filename}.pdf'

    # save figure
    print(f'Save figure to {ffigpath}')
    plt.close(fig)
    fig.savefig(ffigpath)

    # write data
    print(f'Save data to {fdatapath}')
    f = open(fdatapath, "w")
    f.write("#RBW = " + str(spa.band) + " [Hz]" + "\n")
    f.write("#count = " + str(spa.aver_coun) + "\n")
    f.write("#Frequency[Hz] Power[dBm]" + "\n")
    for i in range(len(result.freq)):
        line = '{:f} {}'.format(result.freq[i], result.powDBm[i]) + "\n"
        f.write(line)
        pass
    f.close()

    
    print('End')


if __name__ == '__main__':

    outdir='~/data/n9010a'
    filename=None

    mode = 'SWEEP' # or 'FFT'
    freq_start = 19.99995
    freq_span  = 10.
    rbw = 300.
    npoints = 10001
    nAve = 1

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', dest='mode', type=str, default=mode, help=f'Sweep mode [SWEEP or FFT] (default: {mode})')
    parser.add_argument('-s', '--fstart', dest='freq_start', type=float, default=freq_start, help=f'Start Frequency [GHz] (default: {freq_start})')
    parser.add_argument('-w', '--fspan', dest='freq_span', type=float, default=freq_span, help=f'Frequency Span [kHz] (default: {freq_span})')
    parser.add_argument('-r', '--rbw', dest='rbw', type=float, default=rbw, help=f'Resolution Band-Width (RBW) [Hz] (default: {rbw})')
    parser.add_argument('-p', '--npoints', dest='npoints', default=npoints, type=int, help=f'Number of frequency points (default: {npoints} points)')
    parser.add_argument('-n', '--nAve', dest='nAve', default=nAve, type=int, help=f'Number of measurement counts which will be averaged (default: {nAve} times)')
    parser.add_argument('-o', '--outdir', default=outdir, help=f'Output directory name (default: {outdir})')
    parser.add_argument('--overwrite', default=False, action='store_true', help=f'Overwrite the output files even if there is the same filename data (default: False)')
    parser.add_argument('-i', '--ip_address', default=IP_ADDRESS, help=f'IP address of the Anritsu MS2840A signal analyzer (default: {IP_ADDRESS})')
    parser.add_argument('-f', '--filename', default=filename, help=f'Output filename. If it is None, filename will be asked after measurements. (default: {filename})')
    args = parser.parse_args()


    main(outdir = args.outdir, 
         mode = args.mode,
         start = args.freq_start, #GHz
         stop = args.freq_start + args.freq_span*1.e-6, #GHz
         rbw = args.rbw, # Hz
         npoints = args.npoints, # points
         nAve = args.nAve, # counts
         overwrite = args.overwrite, # do overwrite or not
         ip_address = args.ip_address,
         filename = args.filename);

    pass;
