#!/bin/env python3
import os
import sys
import glob

if __name__=='__main__':
    nargv = len(sys.argv)
    if nargv > 1:
        dirpath = sys.argv[1]
        pass
    if nargv > 2:
        prefix = sys.argv[2]
        pass

    files = glob.glob(f"{dirpath}/{prefix}_*.log")
    #print(files)

    indices = []
    for _file in files:
        #print(_file)
        _index = _file.split(f'{prefix}')[1]
        _index = _index.split('_')[1]
        #print(_index)
        indices.append(_index)
        pass

    if len(flies) > 0:
        print(max(indices))
    else
        print(0)
    pass

