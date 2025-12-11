#!/bin/env python
import os, sys
import socket
import time
import struct
from collections import OrderedDict

class CryomechCPA(object) :
  '''
    Command reference: 
      https://github.com/Cryomech/SampleCode/blob/0f13da3bde63910cef9732fb5b925c9df549c69c/CPA_3xxx_ModbusTCP.py
  '''

  def __init__(self, ip='169.254.87.107', port=502, verbose=0):
    self.ip = ip
    self.port = port
    self.verbose = verbose

    # Associations between keys and their location in rawData
    # Define the order of output
    self.keyloc = OrderedDict([
              ("Operating_State", [9, 10]),
              ("Compressor_State", [11, 12]),
              ("Coolant_In_Temp", [23, 24, 21, 22]),
              ("Coolant_Out_Temp", [27, 28, 25, 26]),
              ("Oil_Temp", [31, 32, 29, 30]),
              ("Helium_Temp", [35, 36, 33, 34]),
              ("Low_Pressure", [39, 40, 37, 38]),
              ("Low_Pressure_Average", [43, 44, 41, 42]),
              ("High_Pressure", [47, 48, 45, 46]),
              ("High_Pressure_Average", [51, 52, 49, 50]),
              ("Delta_Pressure_Average", [55, 56, 53, 54]),
              ("Motor_Current", [59, 60, 57, 58]),
              ("Hours_of_Operation", [63, 64, 61, 62]),
              ("Warning_Number", [113, 114, 111, 112]),
              ("Warning_State", [15, 16, 13, 14]),
              ("Alarm_Number", [117, 118, 115, 116]),
              ("Alarm_State", [19, 20, 17, 18]),
              ("Pressure_Unit", [65, 66]),
              ("Temperature_Unit", [67, 68]),
              ("Serial_Number", [69, 70]),
              ("Model", [71, 72]),
              ("Software_Revision", [73, 74]),
            ])

    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((self.ip, self.port))
    print('CryomechCPA():connect to {}:{}'.format(self.ip, self.port))
    pass

  def __del__(self):
    self.client.close()
    return

  def _convertOperatingState(self, stateNumber):
    strReturn = 'UnknownState'
    if 0 == stateNumber:
      strReturn = 'ReadyTostart'
    elif 2 == stateNumber:
      strReturn = 'Starting'
    elif 3 == stateNumber:
      strReturn = 'Running'
    elif 5 == stateNumber:
      strReturn = 'Stopping'
    elif 6 == stateNumber:
      strReturn = 'ErrorLockout'
    elif 7 == stateNumber:
      strReturn = 'Error'
    elif 8 == stateNumber:
      strReturn = 'HeliumOvertempCooldown'
    elif 9 == stateNumber:
      strReturn = 'PowerRelatedError'
    elif 15 == stateNumber:
      strReturn = 'RecoveredFromError'
    return strReturn 

  def _convertCompressorState(self, stateNumber):
    return 'Running' if 0 < stateNumber else 'Idle' 

  def _convertMessage(self, code):
    strReturn = ''
    worker = code
    if (-1073741824 >= worker):
      strReturn += "InverterCommLoss,"
      worker -= -1073741824
    if (-536870912 >= worker):
      strReturn += "DriverCommLoss,"
      worker -= -536870912
    if (-268435456 >= worker):
      strReturn += "InverterError,"
      worker -= -268435456
    if (-134217728 >= worker):
      strReturn += "MotorCurrentHigh,"
      worker -= -134217728
    if (-67108864 >= worker):
      strReturn += "MotorCurrentSensor,"
      worker -= -67108864
    if (-33554432 >= worker):
      strReturn += "LowPressureSensor,"
      worker -= -33554432
    if (-16777216 >= worker):
      strReturn += "HighPressureSensor,"
      worker -= -16777216
    if (-8388608 >= worker):
      strReturn += "OilSensor,"
      worker -= -8388608
    if (-4194304 >= worker):
      strReturn += "HeliumSensor,"
      worker -= -4194304
    if (-2097152 >= worker):
      strReturn += "CoolantOutSensor,"
      worker -= -2097152
    if (-1048576 >= worker):
      strReturn += "CoolantInSensor,"
      worker -= -1048576
    if (-524288 >= worker):
      strReturn += "MotorStall,"
      worker -= -524288
    if (-262144 >= worker):
      strReturn += "StaticPressureLow,"
      worker -= -262144
    if (-131072 >= worker):
      strReturn += "StaticPressureHigh,"
      worker -= -131072 
    if (-65536 >= worker):
      strReturn += "PowerSupplyError,"
      worker -= -65536 
    if (-32768 >= worker):
      strReturn += "ThreePhaseError,"
      worker -= -32768 
    if (-16384 >= worker):
      strReturn += "MotorCurrentLow,"
      worker -= -16384
    if (-8192 >= worker):
      strReturn += "DeltaPressureLow,"
      worker -= -8192
    if (-4096 >= worker):
      strReturn += "DeltaPressureHigh,"
      worker -= -4096
    if (-2048 >= worker):
      strReturn += "HighPressureLow,"
      worker -= -2048
    if (-1024 >= worker):
      strReturn += "HighPressureHigh,"
      worker -= -1024
    if (-512 >= worker):
      strReturn += "LowPressureLow,"
      worker -= -512
    if (-256 >= worker):
      strReturn += "LowPressureHigh,"
      worker -= -256
    if (-128 >= worker):
      strReturn += "HeliumLow,"
      worker -= -128 
    if (-64 >= worker):
      strReturn += "HeliumHigh,"
      worker -= -64
    if (-32 >= worker):
      strReturn += "OilLow,"
      worker -= -32
    if (-16 >= worker):
      strReturn += "OilHigh,"
      worker -= -16
    if (-8 >= worker):
      strReturn += "CoolantOutLow,"
      worker -= -8
    if (-4 >= worker):
      strReturn += "CoolantOutHigh,"
      worker -= -4
    if (-2 >= worker):
      strReturn += "CoolantInLow,"
      worker -= -2
    if (-1 >= worker):
      strReturn += "CoolantInHigh,"
      worker -= -1
    #remove the final space & Comma if we have a message
    if (0 < len(strReturn.strip())):
      strReturn = strReturn.strip()
      strReturn = strReturn[0:len(strReturn)-1]
    else:
      strReturn = 'None'
    return strReturn

  def _combineBytes(self, bytes_list, locs):
    #combine = '' # for python2
    combine = bytes() # for python3
    #print(bytes_list, type(bytes_list))
    for loc in locs:
      #print(loc, type(loc), bytes_list[loc])
      #combine += bytes_list[loc] # for python2
      combine += bytes([bytes_list[loc]]) # for python3
      pass
    print(combine)
    return combine

  def _convertRawData(self, rawdata, key, locs):
    if key in [
        "Operating_State",
        "Compressor_State",
        "Pressure_Unit",
        "Temperature_Unit",
        "Serial_Number",
        ]:
      data0 = struct.unpack(">H", self._combineBytes(rawdata, locs))[0]
      if key == 'Operating_State':
        data = self._convertOperatingState(data0)
      elif key == 'Compressor_State':
        data = self._convertCompressorState(data0)
      elif key == 'Temperature_Unit':
        if   data0 == 1: data = 'C'
        elif data0 == 2: data = 'K'
        else           : data = 'F'
      elif key == 'Pressure_Unit':
        if   data0 == 1: data = 'Bar'
        elif data0 == 2: data = 'kPa'
        else           : data = 'psi'
      else:
        data = data0
        pass
 
    elif key in ["Warning_Number", "Alarm_Number"]:
      data = struct.unpack(">i", self._combineBytes(rawdata, locs))[0]
      data = self._convertMessage(data)
  
    # 32bit signed integer which is actually stored as a
    # 32bit IEEE float (silly)
    elif key in ["Warning_State", "Alarm_State"]:
      data = int(struct.unpack(">f", self._combineBytes(rawdata, locs))[0])
  
    # 2 x 8-bit lookup tables.
    elif key in ["Model"]:
      model_major = struct.unpack(
          #">B",  rawdata[locs[0]])[0] # for python2
          ">B",  bytes([rawdata[locs[0]]]))[0] # for python3
      model_minor = struct.unpack(
          #">B",  rawdata[locs[1]])[0] # for python2
          ">B",  bytes([rawdata[locs[1]]]))[0] # for python3
      # Model is an attribute, not publishable data
      model = str(model_major) + "_" + str(model_minor)
      data = model
    elif key in ["Software_Revision"]:
      version_major = struct.unpack(
          #">B",  rawdata[locs[0]])[0] # for python2
          ">B",  bytes([rawdata[locs[0]]]))[0] # for python3
      version_minor = struct.unpack(
          #">B",  rawdata[locs[1]])[0] # for python2
          ">B",  bytes([rawdata[locs[1]]]))[0] # for python3
      software_revision = str(version_major) + "." + str(version_minor)
      data = software_revision
 
    # 32 bit Big endian IEEE floating point
    else:
      data = struct.unpack(">f", self._combineBytes(rawdata, locs))[0]
      pass
 
    return data;

  def getKeys(self):
    return self.keyloc.keys()

  def getKeysWtUnit(self):
    keys = self.keyloc.keys()
    keysWtUnit = []
    for key in keys:
      if key in ['Coolant_In_Temp', 
                 'Coolant_Out_Temp', 
                 'Oil_Temp', 
                 'Helium_Temp'
                 ]:
        keysWtUnit.append('{}[{}]'.format(key, self.getTemperatureUnit()))
      elif key in ['Low_Pressure', 
                   'Low_Pressure_Average', 
                   'High_Pressure', 
                   'High_Pressure_Average', 
                   'Delta_Pressure_Average', 
                   ]:
        keysWtUnit.append('{}[{}]'.format(key, self.getPressureUnit()))
      elif key in ['Motor_Current']:
        keysWtUnit.append('{}[A]'.format(key))
      else:
        keysWtUnit.append(key)
        pass
      pass
    return keysWtUnit;
  
  def getStatus(self):
    '''
      Return a list of values related to the status
      The keys can be obtained by getKeys()
    '''
    '''
      query = bytes([0x09, 0x99,  # Message ID
                     0x00, 0x00,  # Unused
                     0x00, 0x06,  # Message size in bytes
                     0x01,        # Slave Address
                     0x04,        # Function Code  3= Read HOLDING registers, 
                                  #                4= Read INPUT registers
                     0x00, 0x01,  # The starting Register Number
                     0x00, 0x37]) # How many to read
    '''
    query = b'\x09\x99\x00\x00\x00\x06\x01\x04\x00\x01\x00\x37'
    self.client.sendall(query)
    response = self.client.recv(1024)
 
    status = []
    for key, locs in self.keyloc.items():
      value = self._convertRawData(response, key, locs)
      status.append(value)
      pass
 
    return status

  def getPressureUnit(self):
    status = self.getStatus()
    index = [ i for i, key in enumerate(self.keyloc.keys()) if key=='Pressure_Unit'][0]
    return status[index]

  def getTemperatureUnit(self):
    status = self.getStatus()
    #print(self.keyloc.keys())
    index = [ i for i, key in enumerate(self.keyloc.keys()) if key=='Temperature_Unit'][0]
    return status[index]

    


if __name__ == '__main__':
  cpa = CryomechCPA()
  print(cpa.getKeys())
  print(cpa.getKeysWtUnit())
  print(cpa.getStatus())
  print(cpa.getPressureUnit())
  print(cpa.getTemperatureUnit())
  pass

