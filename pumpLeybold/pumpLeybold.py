import os
import requests
from tzlocal import get_localzone;
import datetime

def read_pump(ip = '192.168.11.4', timezone=None):
  if timezone is None: timezone = get_localzone();

  url = 'http://{}/!cDS'.format(ip)
  html = requests.get(url)
  # ON : html.text = "0|15|0|5:0,-1;2:0;20:22;4:0,-1;72:3.9e-02;73:0.0e+00;|0,0;50,500|1,0,1,0,0,1,1,1|0|4:0,-1;72:3.9e-02;73:0.0e+00;|0|20"
  # OFF:              0|15|0|5:0,-1;2:0;20:22;4:0,-1;72:2.1e-01;73:0.0e+00;|0,0;0,0|0,0,1,0,0,0,1,1|0|4:0,-1;72:2.1e-01;73:0.0e+00;|0|20
  #print(html.text)
  elements = html.text.split('|')
  value = elements[3].split(';')

  input_power = float(value[0].split(':')[1].split(',')[0]) * (10 ** float(value[0].split(':')[1].split(',')[1]))    # [W]
  frequency = float(value[1].split(':')[1])    # [Hz]
  bearing_temperature = float(value[2].split(':')[1])    # [celsius]
  current = float(value[3].split(':')[1].split(',')[0]) * (10 ** float(value[3].split(':')[1].split(',')[1]))    # [A]
  gauge1_pressure = float(value[4].split(':')[1]) * 100    # [Pa]
  gauge2_pressure = float(value[5].split(':')[1]) * 100    # [Pa]
  time = datetime.datetime.now(timezone)

  pars = {
      'time':time, 
      'power':input_power, #  [W]
      'frequency':frequency, # [Hz]
      'temperature':bearing_temperature, # [deg.]
      'current':current, # [A]
      'pressure1':gauge1_pressure, # [Pa]
      'pressure2':gauge2_pressure, # [Pa]
      }

  return pars


if __name__ == '__main__':
  read_pump()
