#!/bin/env python
# To send calibration data
import os, sys;
import serial;
import json;
import numpy as np;
import array;
from time import sleep;
import datetime;
         
devlocation = '/dev/ttyUSB0'; # for lakeshore218 in tandem PC
# Only writeCalibData()
# calibration data should be created in ROOT-installed  PC.
# This mode is for tandem PC (not ROOT-installed)
# No get log / create json, txt, pdf, calib-data files
# NOTE : Should stop regular obtaining data from lakeshore in crontab when you write the calibration data to the lakeshore.
onlyWriteCalibData = True; 

#outfilename = 'temperature_180521';
#start_cooling_time=datetime.datetime(2018,5,22, 9,10,00);
#stop_cooling_time =datetime.datetime(2018,5,22,13,29,00); # real stop cooling time : 2018/5/22 13:31

outfilename = 'temperature_180530';
start_cooling_time=datetime.datetime(2018,5,30,17,15,00);
#stop_cooling_time =datetime.datetime(2018,5,30,23,30,00);
stop_cooling_time =datetime.datetime(2018,5,30,23,29,00);

outcalibsuffix = '_reduced';

calibTempKey = 'value_4';
dateKey      = 'date_1';
timeKey      = 'time_1';
dtimeKey      = 'dtime';

#channels = [1,2,3,5]; # channel numbers except calibrated channel
channels = [5]; # channel numbers except calibrated channel
curvenames = {
    1:'Input 1 User', 2:'Input 2 User', 3:'Input 3 User', 5:'Input 4 User',

    };
serialnumbers = {
    1:'6079413', 2:'6079365', 3:'6079360', 5:'6079457',
    }
maxCalibPoint = 200 ; # max number of calibration points in lakeshore for each channel

ssleep = sleep(0.1);

defaultverbose = True;

def swrite(serial, string, onlyPrint=False, verbose=defaultverbose) :
  if not string.endswith('\n') :
    string = string+'\n';
    pass;
  if verbose or onlyPrint: print('write "{}"'.format(string[:-1]));
  if not(onlyPrint) :
    ssleep;
    #print('do write "{}"'.format(string[:-1]));
    serial.write(string);
    if not('?' in string) : sleep(0.1); # to wait for lakeshore to finish setting 
    pass;
  pass;

def checkString(string) :
  for i, c in enumerate(string) :
    print('checkString : i={} "{}"'.format(i,c));
    pass;
  pass;

def sread(serial,verbose=defaultverbose) :
  read = '';
  for i in range(100000) :
    read0 = serial.readline();
    read += read0;
    #if len(read0)>0 : print(' read0  : ',['{}'.format(r) for r in read0] );
    if len(read) > 0 and read[-1] == '\n' : break;
    pass;
  if verbose : print 'read : "{string}"'.format(string=read[:-2]);
  return read[:-2];

def splitdata(string) :
  # split string to nn/nn/nn,nn:nnn:nn,+/-nn.nnn,nn,n
  sstring = string.replace(' ','').split(',');
  data = None;
  #print sstring;
  if len(sstring)>4 : 
    data = {
            'date'  : sstring[0], 
            'time'  : sstring[1], 
            'value' : float(sstring[2]), 
            'status': int(sstring[3]  ), 
            'source': int(sstring[4]  ),
           };
  else :
    print('Error!! There are no enough data string in "{}"! Number of components is only {}.'.format(string,len(sstring)+1));
    print('        It should have 4 components.');
    print(' -->> Skip!!');
    pass;
  return data;

def getunit(source) :
  units = ['K', 'degrees', 'V', 'scaled_result'];
  if source-1<len(units) : return units[source-1];
  else                   : return 'nan';

def openSerial() :
  ser = serial.Serial(devlocation, 
          baudrate =9600, 
          timeout  =0, 
          bytesize =serial.SEVENBITS, 
          parity   =serial.PARITY_ODD, 
          stopbits =serial.STOPBITS_ONE, 
          xonxoff  =serial.XOFF
          );
  return ser;

def getdata() :
  ser = openSerial();
  print('check serial');
  print(ser);
  
  print('reset input buffer');
  ssleep;
  ser.reset_input_buffer();
  
  print('print serial name');
  ssleep;
  print(ser.name);
  
  print('check out_waiting');
  ssleep;
  ret = ser.out_waiting;
  print('  out_waiting = {}'.format(ret));
  
  if ser.out_waiting > 0 :
      ssleep();
      ser.reset_output_buffer();
      pass;
  
  # read input device information (for LakeShore Model 218 temperature monitor)
  swrite(ser, '*IDN? 1');
  sread (ser);
  
  # get number of data points
  swrite(ser, 'LOGNUM?');
  Ndata = int(sread(ser));
  print('Ndata = {}'.format(Ndata));
  
  # get logging parameters
  swrite(ser, 'LOGSET?');
  logsetting = sread(ser,True);
  Nreading = int(logsetting.split(',')[-1]);
  
  # for test
  #Ndata = 20;
  
  # get all data
  data = [];
  for idata in xrange(Ndata) :
    one_data = {};
    for j in xrange(1,Nreading+1) :
      swrite(ser, 'LOGVIEW? {} {}'.format(idata,j));
      tmpdata      = sread(ser);
      tmpsplitdata = splitdata(tmpdata);
      if tmpsplitdata!=None :
        one_data['date_{}'  .format(j)] = tmpsplitdata['date'];
        one_data['time_{}'  .format(j)] = tmpsplitdata['time'];
        one_data['value_{}' .format(j)] = tmpsplitdata['value'];
        one_data['status_{}'.format(j)] = tmpsplitdata['status'];
        one_data['source_{}'.format(j)] = tmpsplitdata['source'];
        pass;
      pass;
    #print one_data;
    if len(one_data)>0 : data.append(one_data);
    pass;

  print('close serial');
  ssleep;
  ser.close();

  return data;

def getDateTime(date, time) :
  #print date, time;
  if date.count('/')!=2 : return 0;
  if time.count(':')!=2 : return 0;
  month,   day,  year = date.split('/');
  hour ,minute,second = time.split(':');
  if hour  =='' : hour = 0;
  if minute=='' : minute = 0;
  if second  =='' : second = 0;
  # Modification
  month = (int)(month);
  day   = (int)(day);
  year  = (int)(year.replace('5','201'));
  hour   = (int)(hour);
  minute = (int)(minute);
  second = (int)(second);
  return datetime.datetime(year,month,day,hour,minute,second);

def getOrderedData(data, sortKey, ) :
  data2 = sorted(data, key=lambda x:x[sortKey]);
  return data2;

def getMinMaxData(data, key, isMax=False) :
  temp_value = -1.e+99 if isMax else 1.e+99 ;
  temp_data  = None;
  for point in data :
    #print point;
    value = point[key];
    if isMax and value>temp_value :
      temp_value = value ;
      temp_data  = point ;
      pass;
    if not(isMax) and value<temp_value :
      temp_value = value ;
      temp_data  = point ;
      pass;
    pass;
  #print 'temp_data', temp_data; 
  return temp_data;

def modifyData(data, borderTemp2=25, borderTemp=50, 
    start_cooling_time=datetime.datetime(2018,1,1,0,0,0),
    stop_cooling_time =datetime.datetime(2018,1,2,0,0,0)
    ) :
  # get minimum temperature
  minTemp   = min([ point[calibTempKey] for point in data if point[calibTempKey]>0. ]);
  print('Minimum temperature = {} K'.format(minTemp));
  print('Stop cooling time   = {}'.format(stop_cooling_time));
  Ndata = len(data);
  # data loop : ** new -> old **
  isCooling = False;
  for i, point in enumerate(reversed(data)) :
    temp = point[calibTempKey];
    date = point[dateKey];
    time = point[timeKey];

    print '{} {} / {} K'.format(date, time, temp);
    # Check it is cooling or warming period
    if temp==minTemp : 
      isCooling = True;
      print 'Minimum temperature time : {} {}'.format(date,time);
      print 'Change from cooling duration to rising duration.';
      pass;

    # Remove negative temperature data (extraordinary point)
    if temp<0. : 
      data.remove(point);
      continue;

    # Data with temp. > 50K(borderTemp)
    if temp>borderTemp :
      # Remove odd order points to reduce the number of points
      if i%2==0 :
        data.remove(point);
        continue;
      # Remove rising point with temp. > 50K(borderTemp)
      if not(isCooling) :
        data.remove(point);
        continue;
      pass;

    # Remove the same temperature as in previous point
    pre = Ndata-i;
    if 0<=pre and pre<len(data) and temp==data[pre][calibTempKey] :
      data.remove(point);
      continue;

    # Remove minTemp<temp<25K if it is in cooling process.
    # Use only data point in warming if temp<25K. 
    # -> Remove fluctuation of phase of GM cycle.
    # Not ignore minTemp point
    now_datetime = getDateTime(date,time);
    if now_datetime == 0 :
      print( 'Could not get correct date time from {}, {}.'.format(date, time) );
      print( ' -->> Skip!!' );
      data.remove(point);
      continue;
    if temp<borderTemp :
      #print( 'This data is lower than border temp.={}K'.format(borderTemp) );
      # remove before minTemp
      if isCooling and minTemp<temp : 
        print( 'skip date in cooling duration (before min. temperature)' );
        data.remove(point);
        continue;
      # remove before stop cooling time
      #print now_datetime, stop_cooling_time;
      if now_datetime < stop_cooling_time :
        print( 'skip date in cooling duration (before stop cooling time)' );
        data.remove(point);
        continue;
      pass;

    dtime = (now_datetime - start_cooling_time).seconds / 60. ; # [minuites]
    data[Ndata-i-1][dtimeKey] = dtime;
    #print dtime;
    #print temp, date, time;
    pass;
  # Ordered by temperature
  #print data;
  new_data = getOrderedData(data, calibTempKey);

  def printData(data, description='') :
    #print data;
    print( '{} @ {} {} ({:5.2f} min from cooling start)'.format(description, data[dateKey], data[timeKey], data[dtimeKey]) );
    for i in xrange(99) : 
      if not data.has_key('value_{}'.format(i)) : continue;
      print( '     {}ch : {:5.2f}'.format(i,data['value_{}'.format(i)]) );
      pass;
    return 0;

  mindata = new_data[0];
  printData(data=mindata, description='Minimum temperature in {} ({} K)'.format(calibTempKey, mindata[calibTempKey]));
  for c in channels :
    key = 'value_{}'.format(c);
    mindata = getMinMaxData(data, key, isMax=False);
    #print mindata;
    printData(data=mindata, description='Minimum value in ch {} ({})'.format(c, mindata[key]));
    pass;

  return new_data;


#  drawMaxX2 : x-axis maximum in 2nd pad
def drawData(data,xkey=calibTempKey,xlabel='Temperature [K]',ylabel='Voltage [V]',outsuffix='_V-K',channels=channels, drawMinX2=0, drawMaxX2=4, logy2=False) :
  import ROOT;
  ROOT.gStyle.SetOptStat(0);
  ROOT.gROOT.SetBatch(True);
  colors = [1,2,4,6,7,8,9];
  x        = [ (float)(point[xkey]) for point in data ];
  #print x;
  voltages = [];
  for c in channels :
    voltage    = [ point['value_{}'.format(c)] for point in data ];
    voltages.append(voltage);
    pass;
  x_array = np.array(x);
  #print x_array;
  v_arrays   = [ np.array(voltage) for voltage in voltages ] ;
  npoint     = len(x_array);
  #print npoint, len(v_arrays[0]);

  graphs = [];
  for i in xrange(len(channels)) :
    g = ROOT.TGraph(npoint, x_array, v_arrays[i]);
    graphs.append(g);
    pass;

  def getGraphMaxMin(obj, isMax=True, isX=True, axismin=None, axismax=None) :
    npoint = obj.GetN();
    maxmin = -1.e+10 if isMax else 1.e+10 ;
    for i in xrange(npoint) :
      x = np.array([0.]);
      y = np.array([0.]);
      obj.GetPoint(i,x,y);
      #print x,y;
      if isX :
        # get min/max for x-value
        if axismin!=None and y<axismin : continue;
        if axismax!=None and y>axismax : continue;
        if isMax      and x>maxmin : maxmin = x;
        if not(isMax) and x<maxmin : maxmin = x;
      else   :
        # get min/max for y-value
        if axismin!=None and x<axismin : continue;
        if axismax!=None and x>axismax : continue;
        if isMax      and y>maxmin : maxmin = y;
        if not(isMax) and y<maxmin : maxmin = y;
        pass;
      pass;
    return maxmin;

  def getRange(objects,isX=True,axismin=None,axismax=None) :
    xy = 'x' if isX else 'y';
    if isX :
      l_min = min([ getGraphMaxMin(obj, False, True, axismin, axismax) for obj in objects ]);
      l_max = max([ getGraphMaxMin(obj, True , True, axismin, axismax) for obj in objects ]);
    else :
      l_min = min([ getGraphMaxMin(obj, False, False, axismin, axismax) for obj in objects ]);
      l_max = max([ getGraphMaxMin(obj, True , False, axismin, axismax) for obj in objects ]);
      pass;
    print( '{XY}min = {min0} / {XY}max = {max0}'.format(XY=xy,min0=l_min,max0=l_max) );
    return(l_min,l_max);
 
  # Get x/y range of graphs
  (xmin,xmax) = getRange(graphs,isX=True );
  (ymin,ymax) = getRange(graphs,isX=False);

  def setStyle(g, color, leg=None, legLabel='', legOption='lpe') :
    g.SetMarkerSize(0.5);
    g.SetMarkerStyle(20);
    g.SetMarkerColor(color);
    g.SetLineColor(color);
    g.SetFillColor(color);
    g.SetLineWidth(1);
    if leg!=None : leg.AddEntry(g, legLabel, legOption);
    pass;

  def createAxisHist(xmin=-1e+5,xmax=1e+5,xlabel='Temperature [K]',ylabel='Voltage [V]') :
    hist = ROOT.TH1F('hAxis', '', 10000,xmin,xmax);
    hist.GetXaxis().SetTitle(xlabel);
    hist.GetYaxis().SetTitle(ylabel);
    return hist;

  leg = ROOT.TLegend(0.6,0.6,0.89,0.89);
  leg.SetLineColor(0);
  leg.SetFillStyle(0);
  for i, g in enumerate(graphs) :
    setStyle(g,colors[i],leg,'ch {}'.format(channels[i]), 'pl');
    pass;
  can = ROOT.TCanvas('c1','c1',800,400);
  can.Divide(2,1);

  can.cd(1);
  hAxis = createAxisHist(xmin,xmax,xlabel,ylabel);
  hAxis.GetYaxis().SetRangeUser(ymin,ymax*1.2);

  # Draw pad1
  hAxis.Draw('goff');
  for g in graphs : g.Draw('pl same');
  leg.Draw();

  # Draw pad2
  can.cd(2).SetLogy(logy2);
  hAxis2 = hAxis.DrawClone('goff');
  graphs_2 = [ g.Clone() for g in graphs ];
  for g_2 in graphs_2 : g_2.Draw('pl same');
  xmin2 =  drawMinX2;
  xmax2 =  drawMaxX2;
  hAxis2.GetXaxis().SetRangeUser(xmin2,xmax2);
  (ymin2,ymax2) = getRange(graphs_2,isX=False,axismin=xmin2,axismax=xmax2);
  hAxis2.GetYaxis().SetRangeUser(ymin2,ymax2);

  # Save
  can.Modified();
  can.Update();
  can.SaveAs(outfilename+outsuffix+'.pdf');
  can.SaveAs(outfilename+outsuffix+'.root');
  return 0;

def saveCalibData(data, suffix='') :
  for c in channels :
    outdatafilename = '{}_calibdata_ch{}{}.txt'.format(outfilename,c,suffix);
    if os.path.isfile(outdatafilename) :
      print('Warning!! Calib data file exists! : {}'.format(outdatafilename));
      print('To prevent from removing old calib data file, saveCalibData() is ended!');
      return 1;
      pass;
    outfile = file(outdatafilename,'w') ;
    outfile.write( '# ch{} / {}\n'.format(c,outdatafilename) );
    outfile.write( '# temperature[K] voltage[V]\n' );
    for point in data :
      outfile.write( '{: 11.5f} {: 11.5f}\n'.format(point[calibTempKey], point['value_{}'.format(c)]) );
      pass;
    print( 'Save {} points for ch{}.'.format(len(data),c) );
    outfile.close();
    pass;
  return 0;

def modifyDigit(value, Ndigit) :
  value_str = '';
  if value>=np.power(10,Ndigit-1) : value_str = '{:d}'.format(value);
  else :
    for i in xrange(Ndigit-2,-1,-1) :
      #print i;
      if value>=np.power(10,i) : 
        format_str = '{{:.{}f}}'.format(Ndigit-i-1);
        #print Ndigit,i,format_str;
        value_str  = format_str.format(value);
        break;
      pass;
    pass;
  # case of value<1.
  if value_str=='' : 
    format_str = '{{:.{}f}}'.format(Ndigit-1);
    #print Ndigit,format_str;
    value_str = format_str.format(value);
    pass;
  return value_str;

def writeCalibData(channel, calibfilename,onlyPrint=True) :
  # check calibration data file
  if not( os.path.isfile(calibfilename) ) :
    print( 'Error!! There is no calib data file. : {}'.format(calibfilename) );
    print( ' -->> Skip!!' );
    return 1;
  calibfile = file(calibfilename, 'r');
  points = [];
  # get calibration data
  for line in calibfile :
    line = line.strip();
    if line.startswith('#') : continue;
    temp, voltage = line.split();
    points.append([ (float)(temp), (float)(voltage) ]);
    pass;
  # check number of calibration points
  npoint = len(points);
  if npoint > maxCalibPoint :
    print( 'Error!! Number of calibration points ({} points) for ch{} in {} exceeds '.format(npoint,c,calibfilename) );
    print( '        the max number of calibration points ({} points)that can be recorded in lakeshore.'.format(maxCalibPoint) );
    return 1;
    pass;

  ser = 0;
  if not(onlyPrint) : ser = openSerial();
  # initialize calibration curve
  command = 'CRVHDR? 2{}'.format(c);
  swrite(ser,command,onlyPrint,verbose=True);
  if not(onlyPrint) : sread(ser,verbose=True);
  print( 'Warning!! ch{} curve is deleted. '.format(c) );
  command = 'CRVDEL 2{}'.format(c);
  swrite(ser,command,onlyPrint,verbose=True);
  print( 'Initialize ch{} curve. '.format(c) );
  command = 'CRVHDR 2{},{:15s},{:10s},2,325.0,1'.format(c,curvenames[c],serialnumbers[c]);
  swrite(ser,command,onlyPrint,verbose=True);
  #sleep(1);
  swrite(ser,'CRVHDR? 2{}'.format(c),onlyPrint,verbose=True);
  if not(onlyPrint) : sread(ser,verbose=True);
  
  # Write calibration points
  #print points;
  for i in xrange(maxCalibPoint) :
    #if i>=len(points) : temp, voltage = points[-1];
    if i>=len(points) : continue;
    else              : temp, voltage = points[i];
    command = 'CRVPT 2{},{},{},{}'.format(c,i+1,modifyDigit(voltage,6),modifyDigit(temp,6));
    swrite(ser,command,onlyPrint,verbose=True);
    sleep(0.1);
    swrite(ser,'CRVPT? 2{},{}'.format(c,i+1),onlyPrint,verbose=False);
    if not(onlyPrint) : sread(ser,verbose=True);
    pass;
  if not(onlyPrint) : ser.close();
  return 0;

if __name__=='__main__' :
    
  if not onlyWriteCalibData : 
    if not os.path.isfile(outfilename+'.json') :
      print('get data from lakeshore');
      data= getdata();
      out_json = file(outfilename+'.json','w');
      json.dump(data,out_json);
      out_json.close();
    else :
      print('get data from json file ({}.json)'.format(outfilename));
      in_json = file(outfilename+'.json','r');
      data = json.load(in_json);
      pass;
    Nreading = 0;
    for i in xrange(16) :
      if data[0].has_key('value_{}'.format(i+1)): Nreading=i+1;
      else : break;
      pass;
    print Nreading;
    
    out_txt = file(outfilename+'.txt','w');
    for odata in data :
      out_txt.write('{}:{} '.format(odata['date_1'],odata['time_1']));
      for j in xrange(1,Nreading+1) :
        #print 'source : {}'.format(odata['source_{}'.format(j)]);
        unit = getunit(odata['source_{}'.format(j)]);
        out_txt.write('{}: {} {} '.format(j,odata['value_{}'.format(j)], unit));
        pass;
      out_txt.write('\n');
      pass;
    out_txt.close();
    
    # for 18/05/22 measurement
    #new_data = modifyData(data,borderTemp2=25,borderTemp=50,start_cooling_time=start_cooling_time,stop_cooling_time =stop_cooling_time);
    # for 18/05/30 measurement
    new_data = modifyData(data,borderTemp2=0,borderTemp=50,start_cooling_time=start_cooling_time,stop_cooling_time =stop_cooling_time);
    drawData(new_data,calibTempKey,'Temperature [K]', 'Temperature [K] or Voltage [V]','_V-K',drawMinX2=0,drawMaxX2=4);
    timeOrderedData = getOrderedData(new_data, dtimeKey);
    print '## time ordered data'
    #print timeOrderedData;
    #print [ data[dtimeKey] for data in timeOrderedData ];
    drawData(timeOrderedData,dtimeKey,'Time [min]', 'Temperature [K] or Voltage [V]','_time',channels=[4,5],drawMinX2=0,drawMaxX2=300);
    #drawData(timeOrderedData,dtimeKey,'Time [min]', 'Temperature [K] or Voltage [V]','_time',channels=[1,2,3,4,5],drawMinX2=0,drawMaxX2=300);
    #drawData(timeOrderedData,dtimeKey,'Time [min]', 'Temperature [K]','_time',channels=[1,2,3,4],drawMinX2=250,drawMaxX2=400,logy2=True);
    saveCalibData(new_data,suffix=outcalibsuffix);

    pass ; # end of onlyWriteCalibData

  # write calibration data on lakeshore
  for c in channels :
    calibdatafilename = '{}_calibdata_ch{}{}.txt'.format(outfilename,c,outcalibsuffix);
    writeCalibData(c,calibdatafilename,onlyPrint=False);
    # Test mode (only print command sending to the lakeshore)
    #writeCalibData(c,calibdatafilename,onlyPrint=True);
    pass;

  pass;
  
