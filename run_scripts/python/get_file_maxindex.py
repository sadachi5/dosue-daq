#!/bin/env python3
import os
import sys
import argparse
import glob

def get_file_maxindex(dirpath, prefix, suffix='.log'):
    files = glob.glob(f"{dirpath}/{prefix}_*{suffix}")
    #print(files)

    indices = []
    for _file in files:
        #print(_file)
        _index = _file.split(f'{prefix}')[1]
        _index = _index.split('_')[1]
        #print(_index)
        indices.append((int)(_index))
        pass

    if len(files) > 0:
        maxindex = max(indices)
    else:
        maxindex = 0
        pass
    print(maxindex)
    return maxindex

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='\
        Return maximum index of {dirpath}/{prefix}_{index}_*{suffix} files. \
        Index should be separated by "_".\
    ')
    parser.add_argument('-d', '--dirpath', dest='dirpath', type=str, default='aho', 
        help=f'Search directory (default: aho)')
    parser.add_argument('-p', '--prefix', dest='prefix', type=str, default='DOSUE-Y_Y-factor', 
            help=f'prefix of filename (default: DOSUE-Y_Y-factor)')
    parser.add_argument('-s', '--suffix', dest='suffix', type=str, default='.log', 
        help=f'suffix of filename (default: .log)')
    args = parser.parse_args()

    get_file_maxindex(
            dirpath = args.dirpath,
            prefix = args.prefix,
            suffix = args.suffix
            )
    pass


