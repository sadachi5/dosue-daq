#!/bin/env python3
import os
import sys
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from utils import *

def alphabet2number(alpha):
    row, col = gspread.utils.a1_to_rowcol(f'{alpha}1')
    return col

def main(
        sheetname='2022.10.03_ATF230R1_2-Fh#6_Yfactor',
        outdir='output', outname='2022.10.03_power.pdf'):
    check_dir(outdir)

    ymin=0.
    ymax=0.5e-5
    ylog=False

    volt_min = 459 # mV
    volt_max = 461 # mV
    curr_min = 1400 # mV
    curr_max = 1600 # mV

    # use creds to create a client to interact with the Google Drive API
    scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-access_key.json', scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    #sheet = client.open("DOSUE-Y_SISmixer_test").sheet1
    sheet = client.open("DOSUE-Y_SISmixer_test").worksheet(sheetname)
    # Configurations
    col_prefix = 'A'
    col_LO = 'B'
    col_volt = 'C'
    col_curr = 'D'
    col_Yave = 'F'
    nRun1 = 10
    nRun2 = 10
    csvType1 = 'TwoColumn'
    csvType2 = 'TwoColumn'
    # Input data files
    date = '2022-10-03'
    input_dir = f'/data/ms2840a/{date}/data'

    # Extract values
    data = sheet.get_all_values()
    i_prefix = alphabet2number(col_prefix) - 1
    i_LO = alphabet2number(col_LO) - 1
    i_volt = alphabet2number(col_volt) - 1
    i_curr = alphabet2number(col_curr) - 1
    i_Yave = alphabet2number(col_Yave) - 1

    filepath1_list = []
    filepath2_list = []
    label1_list = []
    label2_list = []
    label1 = '300K'
    label2 = '77K'
    suffix1 = '_300K'
    suffix2 = '_77K'
    for i, line in enumerate(data): 
        if i == 0:
            print('skip 1st line')
            continue
        #print(line)
        try:
            _prefix = line[i_prefix]
            _LO = line[i_LO]
            _volt = (float)(line[i_volt])
            _curr = (float)(line[i_curr])
            _Yave = (float)(line[i_Yave])
            if _volt < volt_min or _volt > volt_max or \
                _curr < curr_min or _curr > curr_max:
                    print('Skip the data because of the voltage & current selection')
                    print(f'voltage: {_volt} ({volt_min}--{volt_max})')
                    print(f'current: {_curr} ({curr_min}--{curr_max})')
                    continue
            _volt = f'{_volt/100.:.3f}'
            _curr = f'{_curr/10.:.1f}'
            _suffix = f'{_LO}GHz_{_volt}mV-{_curr}uA'
            #_filename = f'{_prefix}_{_suffix}'
            _filename = f'{_prefix}_1_{_suffix}'
            _input1 = f'{input_dir}/{_filename}{suffix1}'
            _input2 = f'{input_dir}/{_filename}{suffix2}'
            #_label1 = f'{label1}: {_volt}mV {_curr}uA'
            #_label2 = f'{label2}: {_volt}mV {_curr}uA'
            _label1 = f'{i} Y={_Yave}: {label1}'
            _label2 = f'{i} Y={_Yave}: {label2}'
            print(_LO, _volt, _curr, _suffix)
        except Exception as e:
            print('Warning!:', e)
            print(f'line = {line}')
            print('--> skip the line!')
            continue

        filepath1_list.append( _input1 )
        filepath2_list.append( _input2 )
        label1_list.append( _label1 )
        label2_list.append( _label2 )
        pass

    compare_plot(filepath1_list, filepath2_list,
            label1_list=label1_list, label2_list=label2_list,
            nRun1=nRun1, nRun2=nRun2,
            ymin=ymin, ymax=ymax, ylog=ylog,
            csvType1=csvType1, csvType2=csvType2,
            outdir=outdir, outname=outname)

    return 0

def compare_plot(
        filepath1_list, filepath2_list,
        label1_list=[''], label2_list=[''],
        nRun1=1, nRun2=2,
        csvType1='TwoColumn', csvType2='TwoColumn',
        ymin=0., ymax=None, ylog=False,
        outdir='aho', outname='aho.pdf'):
    check_dir(outdir)
    if len(label1_list) == 1:
        label1_list = [ label1_list[0] for i in range(len(filepath1_list)) ]
        pass
    if len(label2_list) == 1:
        label2_list = [ label2_list[0] for i in range(len(filepath2_list)) ]
        pass

    freq_min = 4. # [GHz]
    freq_max = 12 # [GHz]
    nAve = 50

    freq1_list = []
    freq2_list = []
    power1_list = []
    power2_list = []
    for _filepath in filepath1_list:
        _freq, _power = read_average_nRun(
                _filepath, nRun=nRun1, csvType=csvType1 )
        _freq_ave, tmp = freq_average(_freq, naverage=nAve)
        _power_ave, tmp = freq_average(_power, naverage=nAve)
        freq1_list.append(_freq_ave)
        power1_list.append(_power_ave)
        pass
    for _filepath in filepath2_list:
        _freq, _power = read_average_nRun(
                _filepath, nRun=nRun2, csvType=csvType2 )
        _freq_ave, tmp = freq_average(_freq, naverage=nAve)
        _power_ave, tmp = freq_average(_power, naverage=nAve)
        freq2_list.append(_freq_ave)
        power2_list.append(_power_ave)
        pass
    n1 = len(freq1_list)
    n2 = len(freq2_list)

    default_figure()
    fig, axs = plt.subplots(1,1,squeeze=False)
    fig.set_size_inches(12,6)
    fig.tight_layout();
    plt.subplots_adjust(
            wspace=0.05, hspace=0.30, 
            left=0.10, right=0.95,
            bottom=0.10, top=0.95)

    # Plot each powers
    ax = axs[0][0]
    for i in range(n1):
        _color = cmap(i)
        _freq = freq1_list[i]
        _power = power1_list[i]
        _label = label1_list[i]
        ax.plot(_freq, _power, lw=3, label=_label, ls='-', c=_color)
        pass
    for i in range(n2):
        _color = cmap(i)
        _freq = freq2_list[i]
        _power = power2_list[i]
        _label = label2_list[i]
        ax.plot(_freq, _power, lw=3, label=_label, ls='--', c=_color)
        pass
    default_legend(ax, fontsize=8, ncol=3)
    ax.set_xlabel('Frequency [GHz]')
    ax.set_ylabel('Power [mW]')
    if ymin is not None: ax.set_ylim(ymin = ymin)
    if ymax is not None: ax.set_ylim(ymax = ymax)
    if ylog: ax.set_yscale('log')

    fig.savefig(f'{outdir}/{outname}')
    pass


if __name__ == '__main__':
    main()
    pass
