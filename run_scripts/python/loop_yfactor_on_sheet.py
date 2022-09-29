#!/bin/env python3
import os
import sys
import datetime

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from yfactor_diff2 import yfactor

def alphabet2number(alpha):
    row, col = gspread.utils.a1_to_rowcol(f'{alpha}1')
    return col

def main():
    # use creds to create a client to interact with the Google Drive API
    scope =['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('spreadsheet-access_client-key.json', scope)
    client = gspread.authorize(creds)
    
    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("DOSUE-Y_SISmixer_test").sheet1
    # Configurations
    col_prefix = 'A'
    col_LO = 'B'
    col_volt = 'C'
    col_curr = 'D'
    col_update1 = 'J'
    col_update2 = 'K'
    col_update3 = 'L'
    colI_update1 = alphabet2number(col_update1)
    colI_update2 = alphabet2number(col_update2)
    colI_update3 = alphabet2number(col_update3)
    nRun1 = 10
    nRun2 = 10
    # Input data files
    date = '2022-09-27'
    input_dir = f'/data/ms2840a/{date}/data'
    outdir = f'/data/ms2840a/{date}/figure'

    # Containers for update values
    update1_list = [ '' ] * sheet.row_count
    update2_list = [ '' ] * sheet.row_count
    update3_list = [ '' ] * sheet.row_count

    # Write new columns name
    today = f'{datetime.datetime.now().date()}'
    update1_list[0] = f'Averaged y-factor(Exclude 5--6 GHz) [dB] (update {today})'
    update2_list[0] = f'specific frequency for y-factor [GHz] (update {today})'
    update3_list[0] = f'y-factor at the specific frequency [dB] (update {today})'
    
    # Extract values
    data = sheet.get_all_values()
    i_prefix = alphabet2number(col_prefix) - 1
    i_LO = alphabet2number(col_LO) - 1
    i_volt = alphabet2number(col_volt) - 1
    i_curr = alphabet2number(col_curr) - 1
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
            _volt = f'{_volt/100.:.3f}'
            _curr = f'{_curr/10.:.1f}'
            _suffix = f'{_LO}GHz_{_volt}mV-{_curr}uA'
            _filename = f'{_prefix}_{_suffix}'
            _outname = f'{_filename}_ave_yfactor.pdf'
            _input1 = f'{input_dir}/{_filename}_300K'
            _input2 = f'{input_dir}/{_filename}_77K'
            print(_LO, _volt, _curr, _suffix)
        except Exception as e:
            print('Warning!:', e)
            print(f'line = {line}')
            print('--> skip the line!')
            continue

        _Y, _y, _freq = yfactor(
            outdir = outdir,
            outname = _outname,
            input1 = _input1,
            input2 = _input2,
            nRun1 = nRun1,
            nRun2 = nRun2,
            verbose = -1,
        )
        print(f'(LO:{_LO} GHz, V:{_volt} mV, I:{_curr} uA) : ' +
              f'Averaged Y (exclude 5--6 GHz) = {_Y}, Y @ {_freq} GHz = {_y}')

        # update sheet
        update1_list[i] = f'{_Y:.3f}'
        update2_list[i] = f'{_freq:.6f}'
        update3_list[i] = f'{_y:.3f}'
        pass

    print(update1_list)
    sheet.insert_cols([update1_list], colI_update1)
    sheet.insert_cols([update2_list], colI_update2)
    sheet.insert_cols([update3_list], colI_update3)
    return 0

if __name__ == '__main__':
    main()
    pass
