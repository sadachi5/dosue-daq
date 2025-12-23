#!/bin/env python3
from APSYN420 import APSYN420
ip = '10.10.10.5'

ana = APSYN420(host_ip=ip)
ana.connect()
ana.freq = 20e+9
ana.powerOFF()

ana.close()
