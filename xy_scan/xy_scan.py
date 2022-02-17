# Built-in python modules
import os
import sys
import shutil
import time
import datetime
import argparse
import pathlib
import numpy as np
import pickle

# dosue-daq library
# add PATH to ./src directory
this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(this_dir, '../'))
from Actuator.Actuator import Actuator
from MS2840A.MS2840A import MS2840A
from E8257D.E8257D import E8257D

# Network Configuration
MS2840A_IP_ADDRESS = '192.168.215.248'
E8257D_IP_ADDRESS = '192.168.215.113'


class XYscan:
    """
    XY Scan by an Actuator

    At each (x,y) point, _measure() will run.
    """

    def __init__(self, xy_list, act, spa=None, sg=None, sleep=1, speedrate=0.5, verbose=0):
        self.verbose = verbose
        self.xy_list = xy_list # list of (x,y)
        self.speedrate = speedrate # Actuator speedrate
        self.act = act # Actuator Class
        self.spa = spa # Spectrum Analyzer Class
        self.sg = sg # Signal Generator Class
        self.sleep = sleep # time sleep for each step
        pass

    def __del__(self) :
        return True

    ##################
    # Main functions #
    ##################

    # Scan
    def run_scan(self, outdir=''):

        # create the output directory
        # convert '~/' directory to full path name
        outdir = pathlib.Path(outdir).expanduser() 
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        else:
            # check if you can really overwrite the output directory
            print(f'Warning! The outdir(={outdir}) exists!')
            yn = input('Do you want to replace it to a new data? [y/n]: ')
            if yn == 'y':
                print(f'Remove {outdir} and create a new directory!')
                shutil.rmtree(outdir)
                os.mkdir(outdir)
            else:
                print(f'--> Stop running!')
                return False
            pass

        for i, (x, y) in enumerate(self.xy_list):
            # Define the outfile name
            outfile = f'{outdir}/{i}_{x}_{y}'
            # Move
            self._print(f'run_scan(): Move to ({x},{y})', 0)
            self.act.move(x, y, speedrate=self.speedrate)
            time.sleep(self.sleep)
            # Measure
            self._print(f'run_scan(): Measure at ({x},{y})', 0)
            self._measure(outfile=outfile)
            pass
        return True
  
    ######################
    # Internal functions #
    ######################

    def _writedata(self, result, filename):
        # write data to a dat file
        self._print(f'Save data to {filename}.dat', 1)
        band_wid = self.spa.band_wid
        trace_nAve = self.spa.trace_nAve
        f = open(f'{filename}.dat', "w")
        f.write("#RBW = " + str(band_wid) + " [Hz]" + "\n")
        f.write("#count = " + str(trace_nAve) + "\n")
        f.write("#Frequency[Hz] Power[dBm]" + "\n")
        for i in range(len(result.freq)):
            f.write(str(result.freq[i]) + " " + str(result.powDBm[i]) + "\n")
            pass
        f.close()
        # write data to a pickel file
        self._print(f'Save data to {filename}.pkl', 1)
        band_wid = self.spa.band_wid
        f = open(f'{filename}.pkl', 'wb')
        pickle.dump(result.binary_data, f)
        f.close()
        return True

    # Measure at each (x,y) point
    def _measure(self, outfile):
        # Signal Generator OFF
        self.sg.powerOFF()
        time.sleep(self.sleep)
        # Measure the Spectrum
        result = self.spa.fft_run(verbose=self.verbose)
        self._writedata(result, f'{outfile}_OFF1')

        # Signal Generator ON
        self.sg.powerON()
        time.sleep(self.sleep)
        # Measure the Spectrum 1
        result = self.spa.fft_run(verbose=self.verbose)
        self._writedata(result, f'{outfile}_ON1')
        time.sleep(self.sleep)
        # Measure the Spectrum 2
        result = self.spa.fft_run(verbose=self.verbose)
        self._writedata(result, f'{outfile}_ON2')

        # Signal Generator OFF
        self.sg.powerOFF()
        time.sleep(self.sleep)
        # Measure the Spectrum
        result = self.spa.fft_run(verbose=self.verbose)
        self._writedata(result, f'{outfile}_OFF2')
        
        return True

    # Print message
    def _print(self, msg, threshold_verbose=0):
        if self.verbose > threshold_verbose:
            print(msg)
            pass
        return msg
 

if __name__ == '__main__':
    outdir = '/data/xy_scan/test2'
    freq = 20 # GHz
    verbose = 0

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', type=int, default=verbose, help=f'verbosity level (default: {verbose})')
    parser.add_argument('-o', '--outdir', default=outdir, help=f'Output directory name (default: {outdir})')
    parser.add_argument('-f', '--freq', default=freq, type=int, help=f'Frequency [GHz] (default: {freq})')
    args = parser.parse_args()

    # Frequency Setting
    freq = int(args.freq * 1.e+9) # GHz to Hz
    freq_GHz = freq * 1.e-9 # GHz
    freq_span_kHz = 10.0 # kHz
    rbw = 0.3 # kHz
    meas_time = 1 # sec
    nAve = 1 # Number of average for each data

    # Actuator Setup
    devfile = '/dev/ttyUSB-BlackBox'
    speedrate = 0.5
    act = Actuator(devfile, verbose=args.verbose)
    # Release
    act.release()
    # Homing (NOTE: This is required to know the correct position.)
    act.homing()

    # Spectrum Analyzer Setup
    spa = MS2840A(host_ip = MS2840A_IP_ADDRESS)
    spa.connect()
    spa.fft_setting(
        freq_start=freq_GHz-freq_span_kHz/2.*1.e-6, 
        freq_span=freq_span_kHz,
        rbw=rbw,
        time=meas_time,
        nAve=nAve,
        verbose=0)
    spa.print_fft_setting()

    # Signal Generator Setup
    sg = E8257D(host_ip=E8257D_IP_ADDRESS)
    sg.connect()
    # use x2 multiplier
    sg.freq = freq/2
    sg.power = 5. # dBm
    print(f'frequency = {sg.freq:e} [Hz]')
    print(f'power = {sg.power} [dBm]')
    print(f'power = {sg.power_W} [W]')

    # Create a scan xy list
    x = np.arange(50, 750, 50) # start, stop, step (0<=x<=700) [mm]
    y = np.arange(50, 750, 50) # start, stop, step (0<=y<=900) [mm]
    x_grid, y_grid = np.meshgrid(x, y) # 2D grid in x-axis / y-axis
    xx = x_grid.reshape(-1) # flatten to 1D array
    yy = y_grid.reshape(-1) # flatten to 1D array
    xy_list = np.stack((xx, yy), axis=1) # create list of (x,y)
    # Simple Example
    # xy_list = [(250,250),(250,500),(500,500),(500,250)]
    print(f'x-scan (size: {len(x)}) = {x}')
    print(f'y-scan (size: {len(y)}) = {y}')
    print(f'xy-scan (size: {len(xy_list)}) = {xy_list}')

    xyscan = XYscan(xy_list, act=act, spa=spa, sg=sg, speedrate=speedrate)
    xyscan.run_scan(outdir=args.outdir)
    print(f'Finish XY-scan!')

    del act
    del xyscan
    del spa
    del sg
    pass
