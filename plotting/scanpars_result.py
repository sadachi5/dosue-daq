#!/usr/bin/env python
import os, sys
import argparse
import pathlib
import glob

import socket
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib
from mpl_toolkits.mplot3d import Axes3D

import pandas

plt.ioff()

g_colors = ['tab:blue','tab:orange','tab:green','tab:red','tab:purple',
        'tab:brown','tab:pink','tab:olive','tab:cyan','tab:gray','red',
        'royalblue','turquoise','darkolivegreen','magenta','blue','green']*5

def is_num(s):
    try: 
        float(s)
    except ValueError:
        return False
    else:
        return True

def read_configs(scan_outdir):
    scan_outdir = pathlib.Path(scan_outdir).expanduser()
    print(f'read_configs(): scan output dir = {scan_outdir}')
    csvfilenames = np.array(glob.glob(f'{scan_outdir}/*.csv'))
    print(f'read_configs(): csv files = {csvfilenames}')

    configs = []
    for filename in csvfilenames:
        print(f'read_configs(): read from {filename}')
        csv = np.loadtxt(filename, delimiter=',', comments='#', dtype=str)
        config = {}
        for row in csv:
            data = row[1].strip()
            if is_num(data): config[row[0]] = (float)(data) # convert to float
            else           : config[row[0]] = data # string
            pass
        configs.append(config)
        pass
    print(f'read_configs(): # of configs = {len(configs)}')

    return configs

def create_plot_wt_selections(df, sel_values, sel_key, x_key, y_key, z_key, x_label='', y_label='', z_label=''):
    fig, axs = plt.subplots(3,3)
    fig.set_size_inches(12,12)
    selections = np.array([ df[sel_key]==v for v in sel_values])
    print('selections',len(selections), len(selections[0]))
    selection_any = np.any(selections, axis=0)
    print('selection_any',len(selection_any))
    df_sels = [ df[sel] for sel in selections ]
    df_any  = df[selection_any]
    df_x = df_any[x_key]
    df_y = df_any[y_key]
    x_min = np.min(df_x) * 0.8
    x_max = np.max(df_x) * 1.2
    y_min = np.min(df_y) * 0.8
    y_max = np.max(df_y) * 1.2
    for n, _df in enumerate(df_sels):
        #print(_df.keys())
        print(f'{z_label} ({sel_key}={sel_values[n]}):', _df[['RBW','freq-span','ana-time','count','nRun','filename']])
        i = (int)(n/3.)
        j = n%3
        ax = axs[i][j]
        sc = ax.scatter(_df[x_key], _df[y_key], c=_df[z_key], s=20, cmap=plt.cm.jet)
        for k, v in _df.iterrows():
            ax.annotate(f'{v[z_key]:.1e}', xy=(v[x_key], v[y_key]), size=6)
            pass
        cbar = fig.colorbar(sc, ax=ax)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(f'{z_label} ({sel_key}={sel_values[n]})')
        cbar.set_label(f'{z_label} ({sel_key}={sel_values[n]})', fontsize=12)
        ax.set_xlim([x_min, x_max])
        ax.set_ylim([y_min, y_max])
        ax.grid()
        pass;
    fig.tight_layout()

    return fig

def plot_scanpars_result(configs, outdir, outname='aho'):

    df = pandas.DataFrame(configs)
    df['freq-start'] *= 1.e-9 # GHz
    df['freq-span'] *= 1.e-6 # MHz
    df['RBW'] *= 1.e-3 # kHz
    df['total-time'] = df['ana-time']*df['count']*df['nRun'] # sec
    df['duty-ratio*span'] = df['duty-ratio'] * df['freq-span'] # MHz
    print(df)
    print(df.keys)

    # global selection
    df = df[df['count']==10]

    # check output directory
    outdir = pathlib.Path(outdir).expanduser() # convert '~/' directory to full path name
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
        pass

    # Plotting...
    fig = create_plot_wt_selections(df, sel_values=[1.,2.,5.,10.,20.], sel_key='ana-time', 
            x_key='freq-span', y_key='RBW', z_key='duty-ratio', 
            x_label='Frequency Span [MHz]', y_label='RBW [kHz]', z_label=r'Dutyratio')
    fig.savefig(f'{outdir}/{outname}_freqspan-rbw-dutyratio.pdf')

    fig = create_plot_wt_selections(df, sel_values=[1.,2.,5.,10.,20.], sel_key='ana-time', 
            x_key='freq-span', y_key='RBW', z_key='duty-ratio*span', 
            x_label='Frequency Span [MHz]', y_label='RBW [kHz]', z_label=r'Dutyratio $\times$ Span [MHz]')
    fig.savefig(f'{outdir}/{outname}_freqspan-rbw-dutyratiospan.pdf')

    fig = create_plot_wt_selections(df, sel_values=[1.,2.,5.,10.,20.], sel_key='ana-time', 
            x_key='freq-span', y_key='RBW', z_key='nep', 
            x_label='Frequency Span [MHz]', y_label='RBW [kHz]', z_label='NEP [W/$\sqrt{Hz}$]')
    fig.savefig(f'{outdir}/{outname}_freqspan-rbw-net.pdf')

    fig = create_plot_wt_selections(df, sel_values=[1.,2.,5.,10.,20.], sel_key='ana-time', 
            x_key='freq-span', y_key='RBW', z_key='nep-100kHz', 
            x_label='Frequency Span [MHz]', y_label='RBW [kHz]', z_label='NEP per 100kHz [W/$\sqrt{Hz}$]')
    fig.savefig(f'{outdir}/{outname}_freqspan-rbw-net100kHz.pdf')

    fig = create_plot_wt_selections(df, sel_values=[0.1,0.3,0.5,1.], sel_key='RBW', 
            x_key='freq-span', y_key='ana-time', z_key='duty-ratio', 
            x_label='Frequency Span [MHz]', y_label='Measurement Time [sec]', z_label=r'Dutyratio')
    fig.savefig(f'{outdir}/{outname}_freqspan-time-dutyratio.pdf')

    fig = create_plot_wt_selections(df, sel_values=[0.1,0.3,0.5,1.], sel_key='RBW', 
            x_key='freq-span', y_key='ana-time', z_key='duty-ratio*span', 
            x_label='Frequency Span [MHz]', y_label='Measurement Time [sec]', z_label=r'Dutyratio $\times$ Span [MHz]')
    fig.savefig(f'{outdir}/{outname}_freqspan-time-dutyratiospan.pdf')

    fig = create_plot_wt_selections(df, sel_values=[0.1,0.3,0.5,1.], sel_key='RBW', 
            x_key='freq-span', y_key='ana-time', z_key='nep', 
            x_label='Frequency Span [MHz]', y_label='Measurement Time [sec]', z_label='NEP [W/$\sqrt{Hz}$]')
    fig.savefig(f'{outdir}/{outname}_freqspan-time-net.pdf')

    fig = create_plot_wt_selections(df, sel_values=[0.1,0.3,0.5,1.], sel_key='RBW', 
            x_key='freq-span', y_key='ana-time', z_key='nep-100kHz', 
            x_label='Frequency Span [MHz]', y_label='Measurement Time [sec]', z_label='NEP per 100kHz [W/$\sqrt{Hz}$]')
    fig.savefig(f'{outdir}/{outname}_freqspan-time-net100kHz.pdf')



    return 0


if __name__=='__main__':
    scan_outdir     = '~/data/ms2840a/scan3/2021-10-26/data'
    outdir  = '~/scripts/output/plotting'
    outname = 'scanpars_result'
    
    configs = read_configs(scan_outdir)
    plot_scanpars_result(configs, outdir, outname)

    pass

 
