# Modified on 2025/12/11 for DOSUE-Q beam pattern measurements
# using Anapico APSYN420 + N9010A spectrum analyzer
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
from N9010A.N9010A import N9010A as SPA
from APSYN420.APSYN420 import APSYN420 as SG

# Network Configuration
SPA_IP_ADDRESS = '10.10.10.11'
SG_IP_ADDRESS = '10.10.10.5'
DEVFILE = '/dev/ttyUSB1' # actuator controller openbuilds blackbox

# RF/LO Configuration
RECEIVER_LO = 34e+9 # Hz
SG_MULTIPLIER = 3 # Number of multiplier after the SG
#SG_POWER = None # dBm # Anapico cannot select the power.

# Actuator Configuration
ACTUATOR_XMAX = 750
ACTUATOR_YMAX = 1000


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

        # Actuator setting
        self.act.Xmax = ACTUATOR_XMAX
        self.act.Ymax = ACTUATOR_YMAX
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

        # Open log file
        logfilename = f'{outdir}/run_scan.log'
        with open(logfilename, 'w') as logfile:
            print(f'Open logfile: {logfilename}') 
            logfile.write(f'# date time x y z\n')

            for i, (x, y) in enumerate(self.xy_list):
                # Define the outfile name
                outfile = f'{outdir}/{i}_{x}_{y}'
                # Move
                self._print(f'run_scan(): Move to ({x},{y})', 0)
                self.act.move(x, y, speedrate=self.speedrate)
                _ret, _xyz = self.act.getPosition()
                if not _ret:
                    print('WARNING!: Failed to get position!')
                    x = y = z = 'Nan'
                else:
                    x,y,z = _xyz
                    pass
                time.sleep(self.sleep)
                now = datetime.datetime.now()
                logfile.write(f'{now} {x} {y} {z}\n')
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
        # trace_nAve = self.spa.trace_nAve
        f = open(f'{filename}.dat', "w")
        f.write("#RBW = " + str(band_wid) + " [Hz]" + "\n")
        # f.write("#count = " + str(trace_nAve) + "\n")
        f.write("#Frequency[Hz] Power[dBm]" + "\n")
        for i in range(len(result.freq)):
            f.write(str(result.freq[i]) + " " + str(result.powDBm[i]) + "\n")
            pass
        f.close()
        # write data to a pickel file
        #self._print(f'Save data to {filename}.pkl', 1)
        #band_wid = self.spa.band_wid
        #f = open(f'{filename}.pkl', 'wb')
        #pickle.dump(result.binary_data, f)
        #f.close()
        return True

    # Measure at each (x,y) point
    def _measure(self, outfile):
        # Signal Generator OFF
        self.sg.powerOFF()
        time.sleep(self.sleep)
        # Measure the Spectrum
        result = self.spa.read_data()
        self._writedata(result, f'{outfile}_OFF1')

        # Signal Generator ON
        self.sg.powerON()
        time.sleep(self.sleep)
        # Measure the Spectrum 1
        result = self.spa.read_data()
        self._writedata(result, f'{outfile}_ON1')
        time.sleep(self.sleep)
        # Measure the Spectrum 2
        #result = self.spa.read_data()
        #self._writedata(result, f'{outfile}_ON2')

        # Signal Generator OFF
        #self.sg.powerOFF()
        #time.sleep(self.sleep)
        # Measure the Spectrum
        #result = self.spa.read_data()
        #self._writedata(result, f'{outfile}_OFF2')
        
        return True

    # Print message
    def _print(self, msg, threshold_verbose=0):
        if self.verbose > threshold_verbose:
            print(msg)
            pass
        return msg
 

if __name__ == '__main__':
    outdir = '/DATA/dosue/Q-band/beam_pattern/test/xy_testX'
    freq = 39e+9 # Hz
    verbose = 0

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', dest='verbose', type=int, default=verbose, help=f'verbosity level (default: {verbose})')
    parser.add_argument('-o', '--outdir', default=outdir, help=f'Output directory name (default: {outdir})')
    parser.add_argument('-f', '--freq', default=freq, type=int, help=f'Frequency [Hz] (default: {freq})')
    parser.add_argument('--test', default=False, action='store_true' , help=f'Test run (only checking connection) (default: False)')
    args = parser.parse_args()

    # Frequency Setting
    freq = int(args.freq) # Hz
    freq_GHz = freq * 1.e-9 # GHz
    freq_IF = freq - RECEIVER_LO # Hz
    freq_span = 1.0e+5 # Hz
    rbw = 5.0e+2 # Hz
    # meas_time = 1 # sec # NOT USED FOR N9010A
    npoints = 10001 # NOT USED FOR MS2840A
    nAve = 2 # Number of average for each data

    # Actuator Setup
    speedrate = 0.5
    act = Actuator(DEVFILE, verbose=args.verbose)
    # Release
    act.release()
    # Homing (NOTE: This is required to know the correct position.)
    #act.homing()

    # Spectrum Analyzer Setup
    spa = SPA(host_ip = SPA_IP_ADDRESS)
    spa.connect()

    # For MS2840A case
    #spa.fft_setting(
    #    freq_start=freq_IF-(int)(freq_span/2), 
    #    freq_span=freq_span,
    #    rbw=rbw,
    #    time=meas_time,
    #    nAve=nAve,
    #    verbose=0)
    #spa.print_fft_setting()

    # For N9010A case
    spa.setting(
        freq_start=freq_IF - (int)(freq_span/2), 
        freq_span=(int)(freq_span),
        rbw=rbw,
        npoints=npoints,
        nAve=nAve,
        verbose=1)
 
    # Signal Generator Setup
    sg = SG(host_ip=SG_IP_ADDRESS)
    sg.connect()
    # use x"SG_MULTIPLIER" multiplier
    sg.freq = (int)(freq/SG_MULTIPLIER)
    print(f'frequency = {sg.freq:e} [Hz]')

    # Anapico cannot select the power
    #sg.power = SG_POWER # dBm 
    #print(f'power = {sg.power} [dBm]')
    #print(f'power = {sg.power_W} [W]')

    # Create a scan xy list
    x = np.arange(100, 700 + 100, 100) # start, stop+step, step (0<=x<=750) [mm]
    y = np.arange(100, 700 + 100, 100) # start, stop+step, step (0<=y<=750) [mm]
    #x = np.linspace(2,752,3) # start, stop, # of division (0<=x<=750) [mm]
    #y = np.linspace(2,752,3) # start, stop, # of division (0<=y<=750) [mm]
    #arr1 = np.arange(2,302,50)   # rough mesh
    #arr2 = np.arange(302,512,10) # fine mesh
    #arr3 = np.arange(552,802,50) # rough mesh
    #x = np.hstack([arr1, arr2, arr3])
    #y = np.hstack([arr1, arr2, arr3])
    if args.outdir[-1] == 'X':
        x = np.array([300]) # x = 412 mm only
        y = np.arange(450, 600, 50) # y = 5, 10,..., 750 mm
    elif args.outdir[-1] == 'Y':
        y = np.array([0]) # y = 412 mm only
        x = np.arange(5, 605, 10) # x = 5, 10,..., 750 mm
    #else:
    #    print("ERROR: outdir must end with 'X' or 'Y'")
    #    sys.exit(1)
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
    if not args.test:
        xyscan.run_scan(outdir=args.outdir)
    print(f'Finish XY-scan!')

    del act
    del xyscan
    del spa
    del sg
    pass
