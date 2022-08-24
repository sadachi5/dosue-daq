#!/usr/bin/env python
import os, sys
import argparse
import datetime
import pathlib
import math
import struct
import time
import pickle

import socket
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()

IP_ADDRESS = '10.10.10.2'
PORT = 49153
TIMEOUT = 600

g_colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple',
        'tab:brown','tab:pink','tab:olive','tab:cyan','tab:gray','red',
        'royalblue','turquoise','darkolivegreen','magenta','blue','green']*5

class DATA:
    def __init__(self, powDBm, freq_start, freq_span, MesTimePoint, binary_data=None):
        self._freq = np.linspace(freq_start,freq_start+freq_span,len(powDBm))
        self._powDBm = np.array(powDBm)
        self._time = MesTimePoint
        self._binary_data = binary_data

    @property
    def powDBm(self):
        return self._powDBm

    @property
    def amp(self):
        return np.power(10., self._powDBm*0.1)*1.e-3

    @property
    def freq(self):
        return self._freq

    @property
    def freq_binwidth(self):
        return np.diff(self._freq)

    @property
    def time(self):
        return self._time

    @property
    def binary_data(self):
        return self._binary_data




class MS2840A:
    def __init__(self, host_ip=IP_ADDRESS, port=PORT, timeout=TIMEOUT):
        self._soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._host_ip = host_ip
        self._port = port
        self._connected = False
        self._timeout = timeout
        self._fftmode = None

    def __del__(self):
        if self._connected:
            self.close()
        
    def _w(self, word):
        word += '\r\n'
        self._soc.send(word.encode())

    def _r(self, decode=True, verbose=0):
        if decode:
            ret_msg = ''
            end     = '\r\n'
        else :
            ret_msg = b''
            end     = b'\r\n'
            pass
        while True:
            try:
                rcvmsg = self._soc.recv(1024)
                if verbose>1 : print(f'M2850A:_r(): raw rcvmsg = {rcvmsg}')
                if decode: rcvmsg = rcvmsg.decode()
            except Exception as e:
                print(f'MS2840A:_r(): Error! {e}')
                print(f'MS2840A:_r(): Error! --> Close socket connection!')
                return None
            ret_msg += rcvmsg
            if rcvmsg[-2] == end[0] and rcvmsg[-1] == end[1] :
                break        
        if verbose>1 : print(f'M2850A:_r(): ret_msg = {ret_msg}')
        return ret_msg.strip() if decode else ret_msg[:-2]

    def _wr(self, word, decode=True, verbose=0):
        if verbose>1 : print(f'M2850A:_wr(): command = {word}')
        self._w(word)
        r = self._r(decode=decode, verbose=verbose)
        #if verbose>1 : print(f'M2850A:_wr(): r = {r}')
        if r is None :
            print(f'MS2840A:_wr(): Error! Failed to read for the command: "{word}"')
            print(f'MS2840A:_wr(): Error!  --> Exit')
            self._soc.close()
            return None
            pass
        return r

    def _wait(self):
        self._w('*WAI')

    def print_status(self):
        print('MS2840A:pring_status(): Device identification =', self._wr('*IDN?'))
        print('MS2840A:pring_status(): System Error =', self._wr('SYST:ERR?'))
        print('MS2840A:pring_status(): Event Status =', self._wr('*ESR?'))
        print('MS2840A:pring_status(): SYST:LANG =', self._wr('SYST:LANG?'))
        print('MS2840A:pring_status(): INST =', self._wr('INST?'))
        print('MS2840A:pring_status(): INST:SYST Signal Analyzer   =', self._wr('INST:SYST? SIGANA'))
        print('MS2840A:pring_status(): INST:SYST Spectrum Analyzer =', self._wr('INST:SYST? SPECT'))
        print('MS2840A:pring_status(): INST =', self._wr('INST?'))
        print('MS2840A:pring_status(): Binary order =', self.binary_order)
        
    def print_error(self):
        print('MS2840A:pring_error(): System Error =', self._wr('SYST:ERR?'))

    def default_setting(self):
        print('MS2840A:default_setting(): ')
        print('MS2840A:default_setting(): *** Original status ***')
        self.print_status()
        print('MS2840A:default_setting(): ')
        print('MS2840A:default_setting(): *** Initialize settings')
        self._w('*CLS') # clear
        self._w('*RST') # reset
        self._w('SYST:LANG SCPI')
        print('MS2840A:default_setting(): ')
        print('MS2840A:default_setting(): *** Current status ***')
        self.print_status()
        print('MS2840A:default_setting(): ')
        self.freq_mode = 'NORM'
        self.freqsynt_mode = 'NORM'
        self.is_att_auto = True
        self.is_continu = False
        self.data_format = 'REAL'
        self.binary_order = 'NORM'
        self.print_error()
        self._wait()

    def connect(self):
        if self._connected:
            raise Exception("Already connected.")
        self._soc.connect((self._host_ip, self._port))
        self._soc.settimeout(self._timeout)
        self.default_setting()

    def close(self):
        if self._connected:
            self._soc.close()
            self._connected = False

    def decode_data(self, rawbin, verbose=0):
        nchar = (int)(rawbin[1:2].decode())
        if verbose>1: print(f'MS2840A:decode_data(): nchar = {nchar}')
        nbinary = (int)((int)(rawbin[2:2+nchar].decode())/4)
        unpack_format = '>'+'f'*nbinary
        if verbose>1: 
            print(f'MS2840A:decode_data(): nbinary = {nbinary}')
            print(f'MS2840A:decode_data(): binary data length = {len(rawbin[2+nchar:])}')
            print(f'MS2840A:decode_data(): unpack format = {unpack_format}')
            pass
        data = struct.unpack(unpack_format, rawbin[2+nchar:])
        return data


    def read_data(self, verbose=0):
        ut = time.time()
        # measure data
        self._single()
        data = []
        data_bin = []
        if self._fftmode : 
            npoints = self.trace_points
            nread = math.ceil(npoints/5121.)
            if verbose>0: print(f'MS2840A:read_data(): npoints={npoints}')
            self._soc.settimeout(max(self.capt_time*self.trace_nAve*10, self.timeout))
            for i in range(nread):
                start   = 5121*i
                nremain = npoints - start
                length  = 5121 if nremain>=5121 else nremain
                _rawbin = self._wr(f'TRAC:DATA? {start},{length}', decode=False, verbose=verbose)
                #if verbose>1: print(f'MS2840A:read_data(): _rawbin={_rawbin}')
                _rawdata = self.decode_data(_rawbin, verbose)
                data_bin .append(_rawbin)
                data     +=_rawdata
                pass
            self._soc.settimeout(self.timeout)
        else       : 
            self._soc.settimeout(max(self.sweep_time*self.trace_nAve*10, self.timeout))
            _rawbin = self._wr('TRAC:DATA? TRAC1', decode=False, verbose=verbose)
            data_bin=[_rawbin]
            data    = self.decode_data(_rawbin, verbose)
            self._soc.settimeout(self.timeout)
            pass
        if data is None:
            return None
        data = np.array(data)
        if verbose>0:
            print(f'MS2840A:read_data(): frequency step  = {self.freq_step} Hz')
            print(f'MS2840A:read_data(): RBW  = {self.band_wid} Hz')
            if self._fftmode :
                print(f'MS2840A:read_data(): capture time   = {self.capt_time} sec')
                print(f'MS2840A:read_data(): analysis time  = {self.ana_time} sec')
                print(f'MS2840A:read_data(): IQ data length = {self.measure_time} sec')
                print(f'MS2840A:read_data(): IQ data size   = {self.measure_size} points')
            else :
                pass
            print(f'MS2840A:read_data(): trace points   = {self.trace_points} points')
            print(f'MS2840A:read_data(): sampling rate  = {self.freq_samp} Hz')
            print(f'MS2840A:read_data(): data (size={len(data)}) = {data}')
            if verbose>1 : print(f'MS2840A:read_data(): bainary data (size={len(data_bin)}) = {data_bin}')
        return DATA(data, self.freq_start, self.freq_span, ut, binary_data = data_bin)

    def print_fft_setting(self):
        print('MS2840A:print_fft_setting(): ')
        print('MS2840A:print_fft_setting(): *** fft settings ***')
        print(f'MS2840A:print_fft_setting(): frequency start = {self.freq_start} Hz')
        print(f'MS2840A:print_fft_setting(): frequency stop  = {self.freq_stop} Hz')
        print(f'MS2840A:print_fft_setting(): frequency span  = {self.freq_span} Hz')
        print(f'MS2840A:print_fft_setting(): frequency step  = {self.freq_step} Hz')
        print(f'MS2840A:print_fft_setting(): RBW  = {self.band_wid} Hz')
        print(f'MS2840A:print_fft_setting(): capture time   = {self.capt_time} sec')
        print(f'MS2840A:print_fft_setting(): analysis time  = {self.ana_time} sec')
        print(f'MS2840A:print_fft_setting(): sampling rate  = {self.freq_samp} Hz')
        print(f'MS2840A:print_fft_setting(): trace points   = {self.trace_points} points')
        print(f'MS2840A:print_fft_setting(): # of storage data = {self.trace_nAve} times (averaging {self.trace_nAve} times)')
        print(f'MS2840A:print_fft_setting(): detection mode = {self.det_mode}')
        print(f'MS2840A:print_fft_setting(): data format    = {self.data_format}')
        self.print_error()
        print()

    def fft_setting(self, freq_start, freq_span, rbw, time, att=None, step=None, nAve=1, verbose=0):
        self._fftmode = True
        self._w('INST SIGANA')
        if verbose>0 :
            print('MS2840A:fft_setting(): ')
            print('MS2840A:fft_setting(): *** fft_setting() ***')
            print('MS2840A:fft_setting(): Setup instrument to Signal Analyzer')
            print('MS2840A:fft_setting(): INST =', self._wr('INST?'))
            print('MS2840A:fft_setting(): INST:SYST SIGANA =', self._wr('INST:SYST? SIGANA'))
            print('MS2840A:fft_setting(): ')
            pass
        # Standard setting
        self.is_capt_time_auto = True
        self.is_ana_time_auto = False
        self.ana_start = 0.
        self.trace_mode = 'SPEC'
        self.det_mode   = 'AVER'
        self.data_format = 'REAL'
        # Variable setting
        self.ana_time = 0 # set temporarily
        self.freq_span  = freq_span # [Hz]
        self.band_wid   = rbw # [Hz]
        if step is not None: self.freq_step = step # [Hz]
        if time is not None: self.ana_time = time # [sec]
        if att is not None: self.att = att # [dB]
        else               : 
            print('MS2840A:fft_setting(): Warning! There is no argument of measurement time for one trace.')
            print('MS2840A:fft_setting(): Warning! --> analysis time is set to AUTO.')
            self.is_ana_time_auto = True 
            pass
        self.freq_start = freq_start # [Hz]
        self.trace_nAve = nAve

        if verbose>0 : self.print_fft_setting()
        self._wait()
        return 0

    def fft_run(self, verbose=0):
        if self._fftmode != True:
            print('MS2840A:fft_run(): Error! self._fftmode should be "True" but it is "{self._fftmode}".')
            return None
        self._wait()
        if verbose>0 : self.print_fft_setting()
        data = self.read_data(verbose=verbose)
        return data

    def fft(self, freq_start, freq_span, rbw, time, step=None, nAve=1, verbose=0):
        self.fft_setting(freq_start=freq_start, freq_span=freq_span, rbw=rbw, time=time, step=step, nAve=nAve, verbose=verbose)
        data = self.fft_run(verbose=0)
        return data


    def print_sweep_setting(self):
        print('MS2840A:print_sweep_setting(): ')
        print('MS2840A:print_sweep_setting(): *** sweep settings ***')
        print(f'MS2840A:print_sweep_setting(): frequency start = {self.freq_start} Hz')
        print(f'MS2840A:print_sweep_setting(): frequency stop  = {self.freq_stop} Hz')
        print(f'MS2840A:print_sweep_setting(): frequency span  = {self.freq_span} Hz')
        print(f'MS2840A:print_sweep_setting(): frequency step  = {self.freq_step} Hz')
        print(f'MS2840A:print_sweep_setting(): RBW  = {self.band_wid} Hz')
        print(f'MS2840A:print_sweep_setting(): VBW  = {self.video_wid} Hz')
        print(f'MS2840A:print_sweep_setting(): VBW mode    = {self.video_mode}')
        print(f'MS2840A:print_sweep_setting(): sweep time  = {self.sweep_time} sec')
        print(f'MS2840A:print_sweep_setting(): sweep type  = {self.sweep_type}')
        print(f'MS2840A:print_sweep_setting(): trace points   = {self.trace_points} points')
        print(f'MS2840A:print_sweep_setting(): # of storage data = {self.trace_nAve} times (averaging {self.trace_nAve} times)')
        print(f'MS2840A:print_sweep_setting(): detection mode = {self.det_mode}')
        print(f'MS2840A:print_sweep_setting(): data format    = {self.data_format}')
        self.print_error()
        print('MS2840A:print_sweep_setting(): ')

    def sweep_setting(self, freq_start, freq_stop, rbw, time=None, att=None, step=None, nAve=1, verbose=0):
        self._fftmode = False
        self._w('INST SPECT')
        if verbose>0 :
            print('MS2840A:sweep_setting(): ')
            print('MS2840A:sweep_setting(): *** sweep_setting() ***')
            print('MS2840A:sweep_setting(): Setup instrument to Spectrum Analyzer')
            print('MS2840A:sweep_setting(): INST? =', self._wr('INST?'))
            print('MS2840A:sweep_setting(): INST:SYST =', self._wr('INST:SYST? SPECT'))
            print('MS2840A:sweep_setting(): ')
            pass
        # Standard setting
        self._w('FREQ:OFFS 0') # frequency offset = 0 Hz
        self._w('FREQ:OFFS:STAT 0') # frequency offset: OFF
        self._w('CORR:IMP 50') # impedance = 50 ohm
        self.is_video_wid_auto = True # video band width (VBW): AUTO
        self.video_mode = 'VID' # VIDeo mode
        self._w('CALC:MARK:MODE OFF') # marker mode: Off
        self._w('TRAC:ACT A') # activate trace A
        if time is None : 
            self.is_sweep_auto = True
            self.sweep_automode = 'NORM' # sweep time mode: Normal
        else : 
            self.sweep_time = time
            pass
        if att is not None: self.att = att # [dB]
        self.sweep_type = 'OSWeep' # sweep only mode (no FFT)
        self.data_format = 'REAL'
        # Variable setting
        self.band_wid   = rbw # [Hz]
        if step is not None: self.freq_step = step # [Hz]
        self.freq_start = freq_start # [Hz]
        self.freq_stop  = freq_stop # [Hz]
        self.det_mode = 'RMS' # NORM, POS, NEG, SAMP, RMS
        self.trace_points = (int)((self.freq_stop-self.freq_start)/self.band_wid)*10 + 1
        self.trace_nAve = nAve
        self._wait()

        if verbose>0 : self.print_sweep_setting()
        return 0

    def sweep_run(self, verbose=0):
        if self._fftmode != False :
            print('MS2840A:sweep_run(): Error! self._fftmode should be "False" but it is "{self._fftmode}".')
            return None
        if verbose>0 : self.print_sweep_setting()
        data = self.read_data(verbose=verbose)
        return data

    def sweep(self, freq_start, freq_stop, rbw, time=None, step=None, nAve=1, verbose=0):
        self.sweep_setting(freq_start=freq_start, freq_span=freq_stop, rbw=rbw, time=time, step=step, nAve=nAve, verbose=verbose)
        data = self.sweep_run(verbose=0)
        return data



    # Measurement start

    ## Continuous measurement start
    def _continu_start(self):
        self._w(f'INIT:MODE:CONT')
    ## Single measurement start
    def _single(self):
        self._w(f'INIT:MODE:SING')
        self._wait() # wait for single measurement
    ## Start measurement immediately
    def _imm_start(self):
        self._w(f'INIT') # immediately start by the current mode (continuous or single)
        self._wait() # wait for measurement


    # Time

    @property
    def timeout(self):
        return self._timeout
    @timeout.setter
    def timeout(self, timeout):
        self._timeout = timeout
 
    # Frequency

    @property
    def freq_start(self) :
        return float(self._wr('FREQ:STAR?')) # [Hz]
    @freq_start.setter
    def freq_start(self, freq_Hz):
        self._w(f'FREQ:STAR {freq_Hz}HZ')

    @property
    def freq_stop(self) :
        return float(self._wr('FREQ:STOP?')) # [Hz]
    @freq_stop.setter
    def freq_stop(self, freq_Hz):
        self._w(f'FREQ:STOP {freq_Hz}HZ')

    @property
    def freq_center(self):
        return float(self._wr('FREQ:CENT?')) # [Hz]
    @freq_center.setter
    def freq_center(self, freq_Hz):
        self._w(f'FREQ:CENT {freq_Hz}HZ')

    @property
    def freq_span(self):
        return float(self._wr('FREQ:SPAN?')) # [Hz]
    @freq_span.setter
    def freq_span(self, freq_Hz):
        self._w(f'FREQ:SPAN {freq_Hz}HZ')

    ## Frequency step width
    @property
    def freq_step(self) :
        return float(self._wr('FREQ:CENT:STEP?')) # [Hz]
    @freq_step.setter
    def freq_step(self, step_Hz):
        self._w(f'FREQ:CENT:STEP {step_Hz}HZ')

    ## Auto RBW (Resolution Bandwidth)
    @property
    def is_band_wid_auto(self) -> bool:
        return bool(int(self._wr('BWID:AUTO?')))
    @is_band_wid_auto.setter
    def is_band_wid_auto(self, onoff:bool):
        self._w(f'BWID:AUTO {"1" if onoff else "0"}')
    ## RBW (Resolution Bandwidth)
    @property
    def band_wid(self) :
        return float(self._wr('BWID?')) # [Hz]
    @band_wid.setter
    def band_wid(self, wid_Hz):
        self.is_band_wid_auto = False # AUTO band width OFF
        self._w(f'BWID {wid_Hz}HZ')

    ## Auto VBW (Video Bandwidth, only for SWEEP mode)
    @property
    def is_video_wid_auto(self) -> bool:
        if self._fftmode : return None
        return bool(int(self._wr('BWID:VID:AUTO?')))
    @is_video_wid_auto.setter
    def is_video_wid_auto(self, onoff:bool):
        self._w(f'BWID:VID:AUTO {"1" if onoff else "0"}')
    ## VBW (Video Bandwidth, only for SWEEP mode)
    @property
    def video_wid(self) :
        if self._fftmode : return None
        return float(self._wr('BWID:VID?')) # [Hz]
    @video_wid.setter
    def video_wid(self, wid_Hz):
        self.is_video_wid_auto = 0 # AUTO video width OFF
        self._w(f'BWID:VID {wid_Hz}HZ')
    ## VBW mode (VIDeo or POWer, only for SWEEP mode)
    @property
    def video_mode(self) :
        if self._fftmode : return None
        return str(self._wr('BWID:VID:MODE?')) # [Hz]
    @video_mode.setter
    def video_mode(self, mode):
        if mode in ['VID', 'POW', 'VIDeo', 'POWer']:
            self._w(f'BWID:VID:MODE {mode}')
        else :
            print(f'MS2840A:video_mode(): Error! There is no VBW mode of "{mode}"!')
            pass


    ## Frequency band mode
    @property
    def freq_mode(self) :
        return str(self._wr('FREQ:BAND:MODE?')) # NORMal or SPURious
    @freq_mode.setter
    def freq_mode(self, mode:str):
        if mode in ['NORM', 'SPUR', 'NORMal', 'SPURious']:
            self._w(f'FREQ:BAND:MODE {mode}')
        else :
            print(f'MS2840A:freq_mode(): Error! There is no mode of "{mode}"!')
            pass

    ## Sampling rate
    @property
    def freq_samp(self) :
        if not self._fftmode : return None
        return float(self._wr('FREQ:SRAT?')) # sampling rate [Hz]

    ## Frequency synthesis mode
    @property
    def freqsynt_mode(self) :
        return str(self._wr('FREQ:SYNT?')) # BPHase or NORMal or FAST
    @freqsynt_mode.setter
    def freqsynt_mode(self, mode:str):
        if mode in ['NORM', 'BPH', 'FAST', 'NORMal', 'BPHase']: 
            self._w(f'FREQ:SYNT {mode}')
        else :
            print(f'MS2840A:freqsynt_mode(): Error! There is no frequency synthesis mode of "{mode}"!')
            pass

    # Level

    ## Auto Attenuator 
    @property
    def is_att_auto(self) -> bool:
        return bool(int(self._wr('POW:ATT:AUTO?')))
    @is_att_auto.setter
    def is_att_auto(self, onoff:bool):
        self._w(f'POW:ATT:AUTO {"1" if onoff else "0"}')
    ## Attenuator 
    @property
    def att(self) :
        return float(self._wr('POW:ATT?')) # [dB]
    @att.setter
    def att(self, att_dB):
        self.is_att_auto = False # Auto attenuator OFF
        self._w(f'POW:ATT {att_dB}')

    ## Pre-amp: Not valid for our MS2840A due to lack of preamp
    #@property
    #def is_preamp(self) -> bool:
    #    return bool(int(self._wr('POW:GAIN?')))
    #@is_preamp.setter
    #def is_preamp(self, onoff:bool):
    #    self._w(f'POW:GAIN {"1" if onoff else "0"}')

    # Capture

    ## Auto Capture time
    @property
    def is_capt_time_auto(self) -> bool:
        if not self._fftmode : return None
        return bool(int(self._wr('SWE:TIME:AUTO?')))
    @is_capt_time_auto.setter
    def is_capt_time_auto(self, onoff:bool):
        self._w(f'SWE:TIME:AUTO {"1" if onoff else "0"}')
    ## Capture time
    @property
    def capt_time(self) :
        if not self._fftmode : return None
        return float(self._wr('SWE:TIME?')) # [sec]
    @capt_time.setter
    def capt_time(self, time_sec):
        self.is_capt_time_auto = False # AUTO capture time: OFF
        self._w(f'SWE:TIME {time_sec}S') # [sec]
 
    ## Continuous measurement or not
    @property
    def is_continu(self) -> bool:
        return bool(int(self._wr('INIT:CONT?')))
    @is_continu.setter
    def is_continu(self, onoff:bool):
        self._w(f'INIT:CONT {"1" if onoff else "0"}')

    # Measurement TOD time length
    @property
    def measure_time(self) :
        if not self._fftmode : return None
        return float(self._wr('MMEM:STOR:IQD:LENG?')) # [sec]
    @measure_time.setter
    def measure_time(self, time_sec):
        self._w(f'MMEM:STOR:IQD:LENG {time_sec}S')

    # Measurement TOD sampling size
    @property
    def measure_size(self) :
        if not self._fftmode : return None
        return int(self._wr('MMEM:STOR:IQD:LENG:SAMP?')) # [points]
    @measure_size.setter
    def measure_size(self, size:int):
        self._w(f'MMEM:STOR:IQD:LENG:SAMP {size}')

    # Trace setting

    @property
    def trace_mode(self) :
        return str(self._wr('TRAC:MODE?')) # SPECtrum, PVTime, FVTime, PHASe, CCDF, SPGRam, None
    @trace_mode.setter
    def trace_mode(self, mode:str):
        if mode in ['SPEC', 'PVT', 'FVT', 'CCDF', 'SPGR', 'SPECtrum', 'PVTime', 'FVTime', 'PHASe', 'CCDF', 'SPGRam']: 
            self._w(f'TRAC:mode {mode}')
        else :
            print(f'MS2840A:trace_mode(): Error! There is no trace mode of "{mode}"!')
            pass

    @property
    def is_ana_time_auto(self) -> bool:
        if not self._fftmode : return None
        return bool(int(self._wr('CALC:ATIM:AUTO?')))
    @is_ana_time_auto.setter
    def is_ana_time_auto(self, onoff:bool):
        self._w(f'CALC:ATIM:AUTO {"1" if onoff else "0"}')

    @property
    def ana_time(self) :
        if not self._fftmode : return None
        return float(self._wr('CALC:ATIM:LENG?')) # [sec]
    @ana_time.setter
    def ana_time(self, time_sec):
        self.is_ana_time_auto = False # AUTO analysis time OFF
        self._w(f'CALC:ATIM:LENG {time_sec}') # [sec]

    @property
    def ana_start(self) :
        if not self._fftmode : return None
        return float(self._wr('CALC:ATIM:STAR')) # [sec]
    @ana_start.setter
    def ana_start(self, time_sec):
        self._w(f'CALC:ATIM:START {time_sec}') # [sec]

    ## Trace data points (freq points or TOD points)
    @property
    def trace_points(self) :
        return int(self._wr('SWE:POIN?')) # [points]
    @trace_points.setter
    def trace_points(self, points):
        self._w(f'SWE:POIN {points}')

    @property
    def trace_storemode(self) :
        return self._wr(f'TRAC:STOR:MODE?')
    @trace_storemode.setter
    def trace_storemode(self, mode:str) :
        self._w(f'TRAC:STOR:MODE OFF') 
        if mode in ['OFF', 'MAXH', 'LAV', 'MINH']: # off, store max, store average, store min
            self._w(f'TRAC:STOR:MODE {mode}')
        else :
            print(f'MS2840A:trace_storemode(): Error! There is no trace mode of "{mode}"!')
            pass
    @property
    def trace_nAve(self) -> int:
        if self._nAve>1: return int(self._wr('AVER:COUN?'))
        else           : return self._nAve
    @trace_nAve.setter
    def trace_nAve(self, nAve:int ):
        self._nAve = nAve
        if nAve>1:
            self.trace_storemode = 'LAV' # Trace store mode is chaned to 'average' mode.
            self._w(f'AVER:COUN {nAve}') # range: nAve>=2

    ## Detection mode
    @property
    def det_mode(self) :
        return self._wr('DET?')
    @det_mode.setter
    def det_mode(self, mode:str) :
        if mode in ['NORM', 'POS', 'NEG', 'SAMP', 'AVER', 'RMS', 'NORMal', 'POSitive', 'NEGative', 'SAMPle', 'AVERage']:
            self._w(f'DET {mode}')
        else :
            print(f'MS2840A:det_mode(): Error! There is no detection mode of "{mode}"!')
            pass

    # Sweep setting
    @property
    def sweep_time(self) :
        if self._fftmode : return None
        return float(self._wr('SWE:TIME?'))
    @sweep_time.setter
    def sweep_time(self, time_sec):
        self.is_weep_time_auto = False
        self._w(f'SWE:TIME {time_sec}')

    @property
    def is_sweep_auto(self) -> bool:
        if self._fftmode : return None
        return bool(int(self._wr('SWE:TIME:AUTO?')))
    @is_sweep_auto.setter
    def is_sweep_auto(self, onoff:bool):
        self._w(f'SWE:TIME:AUTO {"1" if onoff else "0"}')

    @property
    def sweep_automode(self) :
        if self._fftmode : return None
        return str(self._wr('SWE:TIME:AUTO:MODE?'))
    @sweep_automode.setter
    def sweep_automode(self, mode):
        if mode in ['NORM', 'FAST', 'NORMal']:
            self._w(f'SWE:TIME:AUTO:MODE {mode}')
        else :
            print(f'MS2840A:sweep_automode(): Error! There is no sweep auto mode of "{mode}"!')

    @property
    def sweep_type(self) :
        if self._fftmode : return None
        return str(self._wr('SWE:RUL?'))
    @sweep_type.setter
    def sweep_type(self, stype):
        if stype in ['DRAN', 'SPE', 'OSW', 'PSW', 'PFFT', 'DRANge', 'SPEed', 'OSWeep', 'PSWeep']:
            self._w(f'SWE:RUL {stype}')
        else :
            print(f'MS2840A:sweep_type(): Error! There is no sweep type of "{stype}"!')

    # Data format
    @property
    def data_format(self) :
        return str(self._wr('FORM?'))
    @data_format.setter
    def data_format(self, form):
        if form in ['REAL', 'ASC', 'ASCii']:
            self._w(f'FORM {form}')
        else :
            print(f'MS2840A:data_format(): Error! There is no data format of "{form}"!')

    @property
    def binary_order(self) :
        return str(self._wr('FORM:BORD?'))
    @binary_order.setter
    def binary_order(self, order): # NORM: big endian / SWAP: little endian
        if order in ['NORM', 'NORMal', 'SWAP', 'SWAPped']:
            self._w(f'FORM:BORD {order}')
        else :
            print(f'MS2840A:binary_order(): Error! There is no binary order type of "{order}"!')


def main(mode='FFT', 
        freq_start = 20e+9,  #Hz
        freq_span  = 2500e+3, #Hz
        rbw        = 300, #Hz
        meas_time  = None, # sec
        att        = None, # dB, None=Auto
        nAve       = 10, # times (number of average for each data)
        nRun       = 10, # times (number of run or saved data)
        outdir='~/data/ms2840a', noplot=False, overwrite=False, shortconfig=False,
        ip_address = IP_ADDRESS,
        filename=None, filename_add_suffix=True, verbose=0):

    # Initialize connection
    ms = MS2840A(host_ip = ip_address)
    ms.connect()

    # Initialize variables
    setting_time = 0
    run_time     = 0

    results = []
    if mode=='FFT' : # FFT mode by using Signal Analyzer

        # parameter setting
        step = 1e+3 # Hz
        # fft setting
        start_time = time.time()
        ms.fft_setting(freq_start=freq_start, freq_span=freq_span, rbw=rbw, time=meas_time, att=att, step=step, nAve=nAve, verbose=verbose+1)
        stop_time = time.time()
        setting_time = stop_time-start_time
        print(f'Elapsed time for fft_setting() = {setting_time} sec')
        # run fft measurement
        start_time = time.time()
        for i in range(nRun):
            print(f'i={i+1}/{nRun} fft_run()')
            result = ms.fft_run(verbose=verbose)
            if result is None :
                print(f'FFT is failed! The return of fft_run is {result}.')
                return 0
            results.append(result)
            pass
        stop_time = time.time()
        run_time  = stop_time - start_time
        print(f'Elapsed time for fft_run() = {run_time} sec')

    elif mode=='SWEEP' :

        # parameter setting
        freq_stop = freq_start + freq_span # Hz
        step      = 1000 # Hz
        # fft setting
        start_time = time.time()
        ms.sweep_setting(freq_start=freq_start, freq_stop=freq_stop, rbw=rbw, time=meas_time, att=att, step=step, nAve=nAve, verbose=verbose+1)
        stop_time = time.time()
        setting_time  = stop_time - start_time
        print(f'Elapsed time for sweep_setting() = {setting_time} sec')
        # run fft measurement
        start_time = time.time()
        for i in range(nRun):
            print(f'i={i+1}/{nRun} sweep_run()')
            result = ms.sweep_run(verbose=verbose)
            if result is None :
                print(f'SWEEP is failed! The return of sweep_run is {result}.')
                return 0
            results.append(result)
            pass
        stop_time = time.time()
        run_time  = stop_time - start_time
        print(f'Elapsed time for sweep_run() = {run_time} sec')

    else :
        print(f'There is no mode for "{mode}". Mode is "FFT" or "SWEEP".')
        ms.close()
        return -1
        pass

    nResult = len(results)

    if not noplot:
        fig, ax = plt.subplots(2,1)
        fig.set_size_inches(6,8)
        for i in range(nResult):
            ax[0].plot(results[i].freq*1e-9, results[i].powDBm, color=g_colors[i], linewidth=1)
            ax[1].plot(results[i].freq*1e-9, results[i].amp   , color=g_colors[i], linewidth=1)
            pass
        ax[0].set_xlabel('Frequency [GHz]')
        ax[0].set_ylabel('Power [dBm]')
        ax[0].grid()
        ax[1].set_xlabel('Frequency [GHz]')
        ax[1].set_ylabel('Power [W]')
        ax[1].grid()
        fig.tight_layout()
        pass

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
    if filename is None or filename=='': filename = input("filename ? : ")
    if filename=='':
        print(f'Do NOT save the data!')
        ms.close()
        plt.close()
        print('End')
        return 0
    if filename_add_suffix :
        filename += f'_{freq_span*1e-3:.1f}MHz_RBW{rbw:.1f}kHz_{nAve}times_{meas_time}sec'
        pass
    fdatapaths = np.array([ f'{todaydir}/data/{filename}_{i}.dat' for i in range(nResult) ] if nResult>1 else [f'{todaydir}/data/{filename}.dat'])
    isexists   = np.array([ os.path.exists(path) for path in fdatapaths ])
    if np.any(isexists) :
        print(f'Warning! The filename(={filename}) exists!')
        if overwrite: _filename = filename;
        else        : _filename = input("other : ")
        if _filename=='':
            print(f'Warning! Do NOT save the data!')
            ms.close()
            plt.close()
            print('End')
            return 0
        elif _filename == filename: print(f'Warning! The output file ({fdatapaths[isexists]}) is overwriten!')
        filename = _filename
        fdatapaths = np.array([ f'{todaydir}/data/{filename}_{i}.dat' for i in range(nResult) ] if nResult>1 else [f'{todaydir}/data/{filename}.dat'])
        pass
    fbinpaths = np.array([ f'{todaydir}/data/{filename}_{i}.pkl' for i in range(nResult) ] if nResult>1 else [f'{todaydir}/data/{filename}.pkl'])
    fconfigpath = f'{todaydir}/data/{filename}.csv'
    ffigpath = f'{todaydir}/figure/{filename}.pdf'

    # save figure
    if not noplot:
        print(f'Save figure to {ffigpath}')
        plt.close(fig)
        fig.savefig(ffigpath)
        pass

    # write data
    print(f'Save data to {fdatapaths}')
    band_wid = ms.band_wid
    trace_nAve = ms.trace_nAve
    for result, fdatapath in zip(results, fdatapaths) :
        f = open(fdatapath, "w")
        f.write("#RBW = " + str(band_wid) + " [Hz]" + "\n")
        f.write("#count = " + str(trace_nAve) + "\n")
        f.write("#Frequency[Hz] Power[dBm]" + "\n")
        for i in range(len(result.freq)):
            f.write(str(result.freq[i]) + " " + str(result.powDBm[i]) + "\n")
            pass
        f.close()
        pass
    for result, fbinpath in zip(results, fbinpaths) :
        f = open(fbinpath, 'wb')
        pickle.dump(result.binary_data, f)
        #for bin_data in bin_data_array:
        #    f.write(bin_data+b'\n')
        #    pass
        f.close()
        pass

    # write config
    print(f'Save data to {fconfigpath}')
    time_str = datetime.datetime.fromtimestamp(result.time).strftime('%Y-%m-%d-%H:%M:%S')
    fftmode = ms._fftmode
    f = open(fconfigpath, "w")
    f.write(f'filename, {filename}, \n')
    for i, path in enumerate(fdatapaths):
        f.write(f'filepath{i}, {path}, \n')
        pass
    freq_binwidth = np.mean(results[0].freq_binwidth)
    f.write(f'start-time, {time_str}, \n')
    f.write(f'mode, {"FFT" if fftmode else "SWEEP"},\n')
    f.write(f'freq-start, {ms.freq_start:e}, Hz\n')
    f.write(f'freq-stop, {ms.freq_stop:e}, Hz\n')
    f.write(f'freq-span, {ms.freq_span:e}, Hz\n')
    f.write(f'freq-step, {ms.freq_step:e}, Hz\n')
    f.write(f'freq-binwidth, {freq_binwidth:e}, Hz\n')
    f.write(f'RBW, {ms.band_wid:e}, Hz\n')
    f.write(f'count, {ms.trace_nAve}, counts\n')
    f.write(f'nRun, {nResult}, times\n')
    f.write(f'trace-points, {ms.trace_points}, points\n')
    f.write(f'trace-mode, {ms.trace_storemode}, \n')
    f.write(f'det-mode, {ms.det_mode}, \n')
    f.write(f'is-att-auto, {ms.is_att_auto}, \n')
    f.write(f'attenuator, {ms.att}, dB\n')
    f.write(f'# FFT setting\n')
    f.write(f'sampling-rate, {ms.freq_samp}, Hz\n')
    f.write(f'capture-time, {ms.capt_time}, sec\n')
    f.write(f'ana-time, {ms.ana_time}, sec\n')
    f.write(f'# SWEEP setting\n')
    f.write(f'sweep-time, {ms.sweep_time}, sec\n')
    f.write(f'sweep-auto, {ms.is_sweep_auto}, \n')
    f.write(f'sweep-automode, {ms.sweep_automode}, \n')
    f.write(f'sweep-type, {ms.sweep_type}, \n')
    f.write(f'VBW, {ms.video_wid}, Hz\n')
    f.write(f'VBW-mode, {ms.video_mode}, Hz\n')
    f.write(f'# Elapsed time\n')
    f.write(f'time-setting, {setting_time}, sec\n')
    f.write(f'time-run, {run_time}, sec\n')
    if not shortconfig: 
        f.write(f'time/MHz, {run_time/(ms.freq_span*1.e-6)}, sec/MHz\n')
        eff_time = ms.ana_time*(float)(ms.trace_nAve*nResult) if fftmode else ms.sweep_time*(float)(ms.trace_nAve*nResult)
        dutyratio = eff_time/run_time;
        f.write(f'duty-ratio, {dutyratio}, \n')
        f.write(f'duty-ratio*span, {dutyratio*(ms.freq_span*1.e-6)}, MHz\n')
        if dutyratio > 0.: 
            f.write(f'span/duty-ratio, {(ms.freq_span*1.e-6)/dutyratio}, MHz\n')
            pass
 
        # Calculate data statistics
        mins  = [ np.min(result.amp) for result in results ] # [W]
        maxs  = [ np.max(result.amp) for result in results ] # [W]
        means = [ np.mean(result.amp) for result in results ] # [W]
        stds  = [ np.std(result.amp) for result in results ] # [W]
        neps  = np.multiply(stds, np.sqrt(eff_time)) # [W*sqrt(sec)]
        nPoints100kHz = (int)(1.e+5/freq_binwidth)
        n100kHz       = (int)(len(results[0].freq)/nPoints100kHz) if nPoints100kHz>0. else 0.
        ampsEvery100kHz = [ result.amp[:nPoints100kHz*n100kHz].reshape(nPoints100kHz,n100kHz) if nPoints100kHz>0 else [] for result in results ]
        stdsEvery100kHz = [ np.mean(np.std(amp, axis=1)) if nPoints100kHz>0 else 0. for amp in ampsEvery100kHz ] # [W] NOTE: Need to check
        nepsEvery100kHz  = np.multiply(stdsEvery100kHz, np.sqrt(eff_time)) # [W*sqrt(sec)]
        f.write(f'# Data statistics\n')
        f.write(f'mean, {np.mean(means):e}, W\n')
        f.write(f'std, {np.mean(stds):e}, W\n')
        f.write(f'std-100kHz, {np.mean(stdsEvery100kHz):e}, W\n')
        f.write(f'nep, {np.mean(neps):e}, W/sqrt(Hz)\n')
        f.write(f'nep-100kHz, {np.mean(nepsEvery100kHz):e}, W/sqrt(Hz)\n')
        f.write(f'min, {np.mean(mins):e}, W\n')
        f.write(f'max, {np.mean(maxs):e}, W\n')
        for i in range(nResult):
            f.write(f'mean{i}, {means[i]:e}, W\n')
            f.write(f'std{i}, {stds[i]:e}, W\n')
            f.write(f'std-100kHz{i}, {stdsEvery100kHz[i]:e}, W\n')
            f.write(f'nep{i}, {neps[i]:e}, W/sqrt(Hz)\n')
            f.write(f'nep-100kHz{i}, {nepsEvery100kHz[i]:e}, W/sqrt(Hz)\n')
            f.write(f'min{i}, {mins[i]:e}, W\n')
            f.write(f'max{i}, {maxs[i]:e}, W\n')
            pass
        pass
    
    ms.close()
    print('End')
    return 0

if __name__ == '__main__':

    # Default settings
    outdir     = '~/data/ms2840a'
    filename   = None
    filename_add_suffix = False
    ## 
    mode = 'SWEEP' # SWEEP or FFT
    freq_start = 18e+9  #Hz
    freq_span  = 8500e+6 #Hz
    rbw        = 1e+6 #Hz
    meas_time  = None # sec (FFT: measurement time / SWEE: sweep time)
    nAve       = 100 # times (averaging number of measurements = counts)
    nRun       = 1 # times (number of run to be recorded separately)

    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', dest='mode', type=str, default=mode, help=f'FFT mode or SWEEP mode (default: {mode})')
    parser.add_argument('-s', '--fstart', dest='freq_start', type=float, default=freq_start, help=f'Start Frequency [Hz] (default: {freq_start})')
    parser.add_argument('-w', '--fspan', dest='freq_span', type=float, default=freq_span, help=f'Frequency Span [Hz] (default: {freq_span})')
    parser.add_argument('-r', '--rbw', dest='rbw', type=float, default=rbw, help=f'Resolution Band-Width (RBW) [Hz] (default: {rbw})')
    parser.add_argument('-t', '--time', dest='meas_time', type=float, default=meas_time, help=f'Measurement/Sweep time for one count for FFT/SWEEP mode [sec] (default: {meas_time})')
    parser.add_argument('-a', '--att', dest='att', type=int, default=None, help=f'Manual attenuation setting [dB] (default: None (auto))')
    parser.add_argument('-n', '--nAve', dest='nAve', default=nAve, type=int, help=f'Number of measurement counts which will be averaged (default: {nAve} times)')
    parser.add_argument('-l', '--nRun', dest='nRun', default=nRun, type=int, help=f'Number of runs to be recorded separately (default: {nRun} times)')
    parser.add_argument('-o', '--outdir', default=outdir, help=f'Output directory name (default: {outdir})')
    parser.add_argument('--noplot', default=False, action='store_true', help=f'Create plots (default: False)')
    parser.add_argument('--overwrite', default=False, action='store_true', help=f'Overwrite the output files even if there is the same filename data (default: False)')
    parser.add_argument('--shortconfig', default=False, action='store_true', help=f'Output csv file has short configuration info. (default: False)')
    parser.add_argument('-i', '--ip_address', default=IP_ADDRESS, help=f'IP address of the Anritsu MS2840A signal analyzer (default: {IP_ADDRESS})')
    parser.add_argument('-f', '--filename', default=filename, help=f'Output filename. If it is None, filename will be asked after measurements. (default: {filename})')
    parser.add_argument('--filename_add_suffix', default=filename_add_suffix, help=f'Add suffix on output filename (default: {filename_add_suffix})')
    parser.add_argument('-v', '--verbose', dest='verbose', default=0, type=int, help=f'Print out verbosity (default: 0)')
    args = parser.parse_args()

    ret = main(
        mode       = args.mode, 
        freq_start = args.freq_start,
        freq_span  = args.freq_span,
        rbw        = args.rbw,
        meas_time  = args.meas_time,
        att        = args.att,
        nAve       = args.nAve,
        nRun       = args.nRun,
        outdir     = args.outdir, 
        noplot     = args.noplot,
        overwrite  = args.overwrite,
        shortconfig= args.shortconfig,
        ip_address = args.ip_address,
        filename   = args.filename,
        filename_add_suffix = args.filename_add_suffix,
        verbose    = args.verbose)

