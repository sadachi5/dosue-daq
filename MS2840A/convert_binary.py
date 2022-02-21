#!/usr/bin/env python
import os, sys
import argparse
import datetime
import pathlib
import math
import struct
import time
import pickle


def decode_data(bindata, verbose=0):
    nchar = (int)(bindata[1:2].decode())
    if verbose>1: 
        print(f'decode_data(): nchar = {nchar}')
        print(f'decode_data(): bindata[2:2+nchar] = {bindata[2:2+nchar]}')
        pass
    nbinary = (int)((int)(bindata[2:2+nchar])/4)
    unpack_format = '>'+'f'*nbinary
    if verbose>1: 
        print(f'decode_data(): nbinary = {nbinary}')
        print(f'decode_data(): binary data length = {len(bindata[2+nchar:])}')
        print(f'decode_data(): unpack format = {unpack_format}')
        pass
    data = struct.unpack(unpack_format, bindata[2+nchar:])
    return data


def convert_binary(filename, outdir='./', outfilename='aho.data'):

    filename = pathlib.Path(filename).expanduser() # convert '~/' directory to full path name
    data = []
    with open(filename, 'rb') as f:
        bindata_set = pickle.load(f)
        print(bindata_set)
        for bindata in bindata_set:
            print(f'bindata = {bindata}')
            __data = decode_data(bindata, verbose=2)
            data += __data
            pass
        print(data)
        pass

    # make output directory
    outdir = pathlib.Path(outdir).expanduser() # convert '~/' directory to full path name
    if not os.path.exists(f'{outdir}'):
        os.makedirs(f'{outdir}')
        pass

    # save data
    outpath = f'{outdir}/{outfilename}'
    with open(outpath, 'w') as f:
        for __data in data:
            f.write(f'{__data}\n')
            pass
        f.close()

    return 0


if __name__ == '__main__':

    # Default settings
    filename   = '~/data/ms2840a/2021-10-31/data/test_FFT_0.pkl'
    outdir     = './output'
    outfilename= 'aho.dat'

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', default=filename, help=f'Input binary filename (default: {filename})')
    parser.add_argument('-o', '--outdir', default=outdir, help=f'Output directory (default: {outdir})')
    parser.add_argument('--outfilename', default=outfilename, help=f'Output filename (default: {outfilename})') 
    args = parser.parse_args()

    convert_binary(filename=args.filename, outdir=args.outdir, outfilename=args.outfilename)

    pass
 
