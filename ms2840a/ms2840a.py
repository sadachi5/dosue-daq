#!/usr/bin/env python
import socket
import numpy as np
from time import sleep
import time
import matplotlib.pyplot as plt
plt.ioff()
import os, sys
import datetime
import pathlib
import math

IP_ADDRESS = '192.168.215.247'
PORT = 49153
TIMEOUT = 100

class DATA:
    def __init__(self, powDBm, freq_start, freq_span, MesTimePoint):
        self._freq = np.linspace(freq_start,freq_start+freq_span,len(powDBm))
        self._powDBm = np.array(powDBm)
        self._time = MesTimePoint

    @property
    def powDBm(self):
        return self._powDBm

    @property
    def amp(self):
        return np.power(10, self._powDBm/10)/1000

    @property
    def freq(self):
        return self._freq

    @property
    def time(self):
        return self._time




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

    def _r(self):
        ret_msg = ''
        self._soc.settimeout(self.timeout)
        while True:
            try:
                rcvmsg = self._soc.recv(1024).decode()
            except Exception as e:
                print(f'MS2840A:_r(): Error! {e}')
                print(f'MS2840A:_r(): Error! --> Close socket connection!')
                return None
            ret_msg += rcvmsg
            if rcvmsg[-1] == '\n':
                break        
        return ret_msg.strip()

    def _wr(self, word):
        self._w(word)
        r = self._r()
        if r is None :
            print(f'MS2840A:_wr(): Error! Failed to read for the command: "{word}"')
            print(f'MS2840A:_wr(): Error!  --> Exit')
            self._soc.close()
            sys.exit(1)
            pass
        return r

    def _wait(self):
        self._w('*WAI')

    def print_status(self):
        print('Device identification =', self._wr('*IDN?'))
        print('System Error =', self._wr('SYST:ERR?'))
        print('Event Status =', self._wr('*ESR?'))
        print('SYST:LANG =', self._wr('SYST:LANG?'))
        print('INST =', self._wr('INST?'))
        print('INST:SYST Signal Analyzer   =', self._wr('INST:SYST? SIGANA'))
        print('INST:SYST Spectrum Analyzer =', self._wr('INST:SYST? SPECT'))
        print('INST =', self._wr('INST?'))
        
    def print_error(self):
        print('System Error =', self._wr('SYST:ERR?'))

    def default_setting(self):
        print()
        print('*** Original status ***')
        self.print_status()
        print()
        print('*** Initialize settings')
        self._w('*CLS') # clear
        self._w('*RST') # reset
        self._w('SYST:LANG SCPI')
        print()
        print('*** Current status ***')
        self.print_status()
        print()
        self.freq_mode = 'NORM'
        self.freqsynt_mode = 'NORM'
        self.is_att_auto = True
        self.is_continu = False
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

    def read_data(self, verbose=0):
        ut = time.time()
        # measure data
        self._single()
        if self._fftmode : 
            npoints = self.trace_points
            nread = math.ceil(npoints/5121.)
            rawstr_array = []
            #print(f'npoints={npoints}')
            for i in range(nread):
                start   = 5121*i
                nremain = npoints - start
                length  = 5121 if nremain>=5121 else nremain
                _rawstr = self._wr(f'TRAC:DATA? {start},{length}')
                rawstr_array.append(_rawstr)
                pass
            rawstr = ','.join(rawstr_array)
        else       : rawstr = self._wr('TRAC:DATA? TRAC1')
        if rawstr is None:
            return None
        data = np.array([float(ns) for ns in rawstr.split(',')])
        if verbose>0:
            print(f'frequency step  = {self.freq_step*1e-3} kHz')
            print(f'RBW  = {self.band_wid*1e-3} kHz')
            if self._fftmode :
                print(f'capture time   = {self.capt_time} sec')
                print(f'analysis time  = {self.ana_time} sec')
                print(f'IQ data length = {self.measure_time} sec')
                print(f'IQ data size   = {self.measure_size} points')
            else :
                pass
            print(f'trace points   = {self.trace_points} points')
            print(f'sampling rate  = {self.freq_samp*1e-3} kHz')
            print(f'data (size={len(data)}) = {data}')
        return DATA(data, self.freq_start, self.freq_span, ut)

    def print_fft_setting(self):
        print()
        print('*** fft settings ***')
        print(f'frequency start = {self.freq_start*1e-9} GHz')
        print(f'frequency stop  = {self.freq_stop*1e-9} GHz')
        print(f'frequency span  = {self.freq_span*1e-3} kHz')
        print(f'frequency step  = {self.freq_step*1e-3} kHz')
        print(f'RBW  = {self.band_wid*1e-3} kHz')
        print(f'capture time   = {self.capt_time} sec')
        print(f'analysis time  = {self.ana_time} sec')
        print(f'sampling rate  = {self.freq_samp*1e-3} kHz')
        print(f'trace points   = {self.trace_points} points')
        print(f'# of storage data = {self.trace_nave} times (averaging {self.trace_nave} times)')
        print(f'detection mode = {self.det_mode}')
        self.print_error()
        print()

    def fft_setting(self, freq_start, freq_span, rbw, time, step=None, nave=1, verbose=0):
        self._fftmode = True
        self._w('INST SIGANA')
        if verbose>0 :
            print()
            print('*** fft_setting() ***')
            print('Setup instrument to Signal Analyzer')
            print('INST =', self._wr('INST?'))
            print('INST:SYST SIGANA =', self._wr('INST:SYST? SIGANA'))
            print()
            pass
        # Standard setting
        self.is_capt_time_auto = True
        self.is_ana_time_auto = False
        self.ana_start = 0.
        self.trace_mode = 'SPEC'
        self.det_mode   = 'AVER'
        # Variable setting
        if time is not None: self.ana_time = time # [sec]
        else               : 
            print('MS2840A:fft_setting(): Warning! There is no argument of measurement time for one trace.')
            print('MS2840A:fft_setting(): Warning! --> analysis time is set to AUTO.')
            self.is_ana_time_auto = True 
            pass
        self.freq_span  = freq_span # [GHz]
        self.band_wid   = rbw # [kHz]
        if step is not None: self.freq_step = step # [kHz]
        self.freq_start = freq_start # [GHz]
        self.trace_nave = nave

        if verbose>0 : self.print_fft_setting()
        self._wait()
        return 0

    def fft_run(self, verbose=0):
        if self._fftmode is None :
            print('MS2840A:fft_run(): Error! fft or sweep mode (self._fftmode) is not set.')
            return None
        self._wait()
        if verbose>0 : self.print_fft_setting()
        data = self.read_data(verbose=verbose)
        return data

    def fft(self, freq_start, freq_span, rbw, time, step=None, nave=1, verbose=0):
        self.fft_setting(freq_start=freq_start, freq_span=freq_span, rbw=rbw, time=time, step=step, nave=nave, verbose=verbose)
        data = self.fft_run(verbose=0)
        return data


    def print_sweep_setting(self):
        print()
        print('*** sweep settings ***')
        print(f'frequency start = {self.freq_start*1e-9} GHz')
        print(f'frequency stop  = {self.freq_stop*1e-9} GHz')
        print(f'frequency span  = {self.freq_span*1e-3} kHz')
        print(f'frequency step  = {self.freq_step*1e-3} kHz')
        print(f'RBW  = {self.band_wid*1e-3} kHz')
        print(f'VBW  = {self.video_wid*1e-3} kHz')
        print(f'VBW mode    = {self.video_mode}')
        print(f'sweep time  = {self.sweep_time} sec')
        print(f'sweep type  = {self.sweep_type}')
        print(f'trace points   = {self.trace_points} points')
        print(f'# of storage data = {self.trace_nave} times (averaging {self.trace_nave} times)')
        print(f'detection mode = {self.det_mode}')
        self.print_error()
        print()

    def sweep_setting(self, freq_start, freq_stop, rbw, time=None, step=None, nave=1, verbose=0):
        self._fftmode = False
        self._w('INST SPECT')
        if verbose>0 :
            print()
            print('*** sweep_setting() ***')
            print('Setup instrument to Spectrum Analyzer')
            print('INST? =', self._wr('INST?'))
            print('INST:SYST =', self._wr('INST:SYST? SPECT'))
            print()
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
        self.sweep_type = 'OSWeep' # sweep only mode (no FFT)
        # Variable setting
        self.band_wid   = rbw # [kHz]
        if step is not None: self.freq_step = step # [kHz]
        self.freq_start = freq_start # [GHz]
        self.freq_stop  = freq_stop # [GHz]
        self.det_mode = 'RMS' # NORM, POS, NEG, SAMP, RMS
        self.trace_points = (int)((self.freq_stop-self.freq_start)/self.band_wid) + 1
        self.trace_nave = nave
        self._wait()

        if verbose>0 : self.print_sweep_setting()
        return 0

    def sweep_run(self, verbose=0):
        if self._fftmode is None :
            print('MS2840A:fft_run(): Error! fft or sweep mode (self._fftmode) is not set.')
            return None
        if verbose>0 : self.print_sweep_setting()
        data = self.read_data(verbose=verbose)
        return data

    def sweep(self, freq_start, freq_stop, rbw, time=None, step=None, nave=1, verbose=0):
        self.sweep_setting(freq_start=freq_start, freq_span=freq_stop, rbw=rbw, time=time, step=step, nave=nave, verbose=verbose)
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
    def freq_start(self, freq_GHz):
        self._w(f'FREQ:STAR {freq_GHz}GHZ')

    @property
    def freq_stop(self) :
        return float(self._wr('FREQ:STOP?')) # [Hz]
    @freq_stop.setter
    def freq_stop(self, freq_GHz):
        self._w(f'FREQ:STOP {freq_GHz}GHZ')

    @property
    def freq_center(self):
        return float(self._wr('FREQ:CENT?')) # [Hz]
    @freq_center.setter
    def freq_center(self, freq_GHz):
        self._w(f'FREQ:CENT {freq_GHz}GHZ')

    @property
    def freq_span(self):
        return float(self._wr('FREQ:SPAN?')) # [Hz]
    @freq_span.setter
    def freq_span(self, freq_kHz):
        self._w(f'FREQ:SPAN {freq_kHz}KHZ')

    ## Frequency step width
    @property
    def freq_step(self) :
        return float(self._wr('FREQ:CENT:STEP?')) # [Hz]
    @freq_step.setter
    def freq_step(self, step_kHz):
        self._w(f'FREQ:CENT:STEP {step_kHz}KHZ')

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
    def band_wid(self, wid_kHz):
        self.is_band_wid_auto = 0 # AUTO band width OFF
        self._w(f'BWID {wid_kHz}KHZ')

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
    def video_wid(self, wid_kHz):
        self.is_video_wid_auto = 0 # AUTO video width OFF
        self._w(f'BWID:VID {wid_kHz}KHZ')
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
    def trace_nave(self) -> int:
        return int(self._wr('AVER:COUN?'))
    @trace_nave.setter
    def trace_nave(self, nave:int ):
        self.trace_storemode = 'LAV' # Trace store mode is chaned to 'average' mode.
        self._w(f'AVER:COUN {nave}')

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
        self._w(f'SWE:RUL {stype}')
        if stype in ['DRAN', 'SPE', 'OSW', 'PSW', 'PFFT', 'DRANge', 'SPEed', 'OSWeep', 'PSWeep']:
            self._w(f'SWE:RUL {stype}')
        else :
            print(f'MS2840A:sweep_type(): Error! There is no sweep type of "{stype}"!')




def main(mode='FFT', 
        freq_start = 20.,  #GHz
        freq_span  = 2.5e+3, #kHz
        rbw        = 0.3, #kHz
        meas_time  = None, # sec
        nave       = 10, # times
        outdir='~/data/ms2840a', filename_add_suffix=True):

    # Initialize connection
    ms = MS2840A()
    ms.connect()

    # Initialize variables
    setting_time = 0
    run_time     = 0

    if mode=='FFT' : # FFT mode by using Signal Analyzer

        # parameter setting
        step = rbw # kHz
        # fft setting
        start_time = time.time()
        result = ms.fft_setting(freq_start=freq_start, freq_span=freq_span, rbw=rbw, time=meas_time, step=step, nave=nave, verbose=1)
        stop_time = time.time()
        setting_time = stop_time-start_time
        print(f'Elapsed time for fft_setting() = {setting_time} sec')
        # run fft measurement
        start_time = time.time()
        result = ms.fft_run(verbose=0)
        if result is None :
            print(f'FFT is failed! The return of fft_run is {result}.')
            return 0
        stop_time = time.time()
        run_time  = stop_time - start_time
        print(f'Elapsed time for fft_run() = {run_time} sec')

    elif mode=='SWEEP' :

        # parameter setting
        freq_stop = freq_start + freq_span*1e-6 # GHz
        step      = None # kHz
        # fft setting
        start_time = time.time()
        result = ms.sweep_setting(freq_start=freq_start, freq_stop=freq_stop, rbw=rbw, time=meas_time, step=step, nave=nave, verbose=1)
        stop_time = time.time()
        setting_time  = stop_time - start_time
        print(f'Elapsed time for sweep_setting() = {setting_time} sec')
        # run fft measurement
        start_time = time.time()
        result = ms.sweep_run(verbose=0)
        if result is None :
            print(f'SWEEP is failed! The return of sweep_run is {result}.')
            return 0
        stop_time = time.time()
        run_time  = stop_time - start_time
        print(f'Elapsed time for sweep_run() = {run_time} sec')

    else :
        print(f'There is no mode for "{mode}". Mode is "FFT" or "SWEEP".')
        ms.close()
        return -1
        pass


    fig, ax = plt.subplots()
    ax.plot(result.freq*1e-9, result.powDBm)
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
    filename = input("filename ? : ")
    if filename=='':
        print(f'Do NOT save the data!')
        ms.close()
        plt.close()
        print('End')
        return 0
    if filename_add_suffix :
        filename += f'_{freq_span*1e-3:.1f}MHz_RBW{rbw:.1f}kHz_{nave}times_{meas_time}sec'
        pass
    fdatapath = f'{todaydir}/data/{filename}.dat'
    if os.path.exists(fdatapath):
        _filename = input("other : ")
        if _filename == filename: print(f'Warning! The output file ({filename}.dat) is overwriten!')
        filename = _filename
        fdatapath = f'{todaydir}/data/{filename}.dat'
        pass
    fconfigpath = f'{todaydir}/data/{filename}.csv'
    ffigpath = f'{todaydir}/figure/{filename}.pdf'

    # save figure
    print(f'Save figure to {ffigpath}')
    plt.close(fig)
    fig.savefig(ffigpath)

    # write data
    print(f'Save data to {fdatapath}')
    f = open(fdatapath, "w")
    f.write("#RBW = " + str(ms.band_wid) + " [Hz]" + "\n")
    f.write("#count = " + str(ms.trace_nave) + "\n")
    f.write("#Frequency[Hz] Power[dBm]" + "\n")
    for i in range(len(result.freq)):
        f.write(str(result.freq[i]) + " " + str(result.powDBm[i]) + "\n")
        pass
    f.close()

    # write config
    print(f'Save data to {fconfigpath}')
    time_str = datetime.datetime.fromtimestamp(result.time).strftime('%Y-%m-%d-%H:%M:%S')
    fftmode = ms._fftmode
    f = open(fconfigpath, "w")
    f.write(f'filename, {filename}, \n')
    f.write(f'start-time, {time_str}, \n')
    f.write(f'mode, {"FFT" if fftmode else "SWEEP"},\n')
    f.write(f'freq-start, {ms.freq_start}, Hz\n')
    f.write(f'freq-stop, {ms.freq_stop}, Hz\n')
    f.write(f'freq-span, {ms.freq_span}, Hz\n')
    f.write(f'freq-step, {ms.freq_step}, Hz\n')
    f.write(f'RBW, {ms.band_wid}, Hz\n')
    f.write(f'count, {ms.trace_nave}, counts\n')
    f.write(f'trace-points, {ms.trace_points}, points\n')
    f.write(f'trace-mode, {ms.trace_storemode}, \n')
    f.write(f'det-mode, {ms.det_mode}, \n')
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
    f.write(f'time/MHz, {run_time/(ms.freq_span*1.e-6)}, sec/MHz\n')
    dutyratio = (ms.ana_time*(float)(ms.trace_nave))/run_time if fftmode else (ms.sweep_time*(float)(ms.trace_nave))/run_time;
    f.write(f'duty-ratio, {dutyratio}, \n')
    f.write(f'duty-ratio*span, {dutyratio*(ms.freq_span*2.e-6)}, MHz\n')
    f.write(f'span/duty-ratio, {(ms.freq_span*1.e-6)/dutyratio}, MHz\n')
    
    ms.close()
    print('End')
    return 0

if __name__ == '__main__':

    outdir='~/data/ms2840a'
    filename_add_suffix = False

    # SWEEP
    '''
    mode = 'SWEEP' # SWEEP or FFT
    freq_start = 19.99995 #GHz
    freq_span  = 1.e+2 #kHz
    rbw        = 0.3 #kHz
    meas_time  = None # sec only for FFT
    nave       = 1 # times
    #'''

    # FFT
    #'''
    mode = 'FFT' # SWEEP or FFT
    freq_start = 19.99995  #GHz
    freq_span  = 1.e+2 #kHz
    rbw        = 1 #kHz
    meas_time  = 1 # sec only for FFT
    nave       = 10 # times
    #'''


    ret = main(mode=mode, 
        freq_start = freq_start,
        freq_span  = freq_span,
        rbw        = rbw,
        meas_time  = meas_time,
        nave       = nave,
        outdir     = outdir, 
        filename_add_suffix=filename_add_suffix)

