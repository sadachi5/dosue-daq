#!/bin/env python
import os, sys
import socket
import time
import binascii
import struct

host = '169.254.87.107';

port = 502

def combineBytes(bytes_list, locs):
  combine = ''
  for loc in locs:
    combine += bytes_list[loc]
    pass
  #print(combine)
  return combine

def convertRawData(rawdata, key, locs):
  if key in [
      "Operating_State",
      "Compressor_State",
      "Pressure_Unit",
      "Temperature_Unit",
      "Serial_Number",
      ]:
    data0 = struct.unpack(">H", combineBytes(rawdata, locs))[0]
    if key == 'Temperature_Unit':
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

  # 32bit signed integer which is actually stored as a
  # 32bit IEEE float (silly)
  elif key in ["Warning_State", "Alarm_State"]:
    data = int(struct.unpack(">f", combineBytes(rawdata, locs))[0])
  # 2 x 8-bit lookup tables.
  elif key in ["Model"]:
    model_major = struct.unpack(
        ">B",  rawdata[locs[0]])[0]
    model_minor = struct.unpack(
        ">B", rawdata[locs[1]])[0]
    # Model is an attribute, not publishable data
    model = str(model_major) + "_" + str(model_minor)
    data = model
  elif key in ["Software_Revision"]:
    version_major = struct.unpack(
        ">B", rawdata[locs[0]])[0]
    version_minor = struct.unpack(
        ">B", rawdata[locs[1]])[0]
    software_revision = str(version_major) + "." + str(version_minor)
    data = software_revision
  # 32 bit Big endian IEEE floating point
  else:
    data = struct.unpack(">f", combineBytes(rawdata, locs))[0]
    pass
  return data;



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

# Power OFF
'''
query = bytes([0x09, 0x99,  # Message ID
               0x00, 0x00,  # Unused
               0x00, 0x06,  # Message size in bytes
               0x01,        # Slave Address
               0x06,        # Function Code  6= Write a single Holding register
               0x00, 0x01,  # The starting Register Number
               0x00, 0x01]) # How many to read
'''
query = b'\x09\x99\x00\x00\x00\x06\x01\x06\x00\x01\x00\xff' # The last 2 bits represent command.
client.sendall(query)
response = client.recv(1024)

# Check Status
query = b'\x09\x99\x00\x00\x00\x06\x01\x04\x00\x01\x00\x37'
client.sendall(query)
response = client.recv(1024)

# Associations between keys and their location in rawData
keyloc = {"Operating_State": [9, 10],
          "Compressor_State": [11, 12],
          "Warning_State": [15, 16, 13, 14],
          "Alarm_State": [19, 20, 17, 18],
          "Coolant_In_Temp": [23, 24, 21, 22],
          "Coolant_Out_Temp": [27, 28, 25, 26],
          "Oil_Temp": [31, 32, 29, 30],
          "Helium_Temp": [35, 36, 33, 34],
          "Low_Pressure": [39, 40, 37, 38],
          "Low_Pressure_Average": [43, 44, 41, 42],
          "High_Pressure": [47, 48, 45, 46],
          "High_Pressure_Average": [51, 52, 49, 50],
          "Delta_Pressure_Average": [55, 56, 53, 54],
          "Motor_Current": [59, 60, 57, 58],
          "Hours_of_Operation": [63, 64, 61, 62],
          "Pressure_Unit": [65, 66],
          "Temperature_Unit": [67, 68],
          "Serial_Number": [69, 70],
          "Model": [71, 72],
          "Software_Revision": [73, 74]}

for key, locs in keyloc.items():
  value = convertRawData(response, key, locs)
  print( '{} = {}'.format(key, value) )
  pass;






"""


import traceback
for i in xrange(0,254) :
  host = '169.254.178.{}'.format(i);
  print(host);
  try :
    client.connect((host,port));
  except :
    print('error');
    traceback.print_exc()
    pass;
  pass;
"""
