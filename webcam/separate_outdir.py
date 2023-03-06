#!/bin/python
import os, sys;

checkdir = '/data/webcam/';
files = os.listdir(checkdir);
print files[:4];


for filename in files : 
  splitfilename = filename.split(':');
  if len(splitfilename) < 3 : continue;
  year  = splitfilename[0];
  month = splitfilename[1];
  day   = splitfilename[2].split('-')[0];
  newdir = '{}{}{}'.format( year, month, day );
  newdirpath = checkdir+'/'+newdir;
  if not os.path.isdir(newdirpath) :
    os.mkdir(newdirpath);
    pass;
  cmd = 'mv {indir}/{file} {outdir}/{file}'.format( indir=checkdir, file=filename, outdir=newdirpath );
  print cmd; 
  os.system(cmd);
  pass;

