'''
Date: 2022-11-29 17:18:01
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-16 15:17:26
FilePath: /testdata/5-template.py
'''
import os
import sys
import glob
import subprocess
import shutil
import csv
import datetime
#from datetime import datetime
#from obspy import read
import shutil

path="/home/cugfm/data/testdata"
trace="/home/cugfm/data/testdata/Trace/"
template="/home/cugfm/data/testdata/Template"
os.chdir(path)

#---------------------------template window length paramater
b=-5
a=40

#-----------------------------------read event
ecsv_file = csv.reader(open("IBR_eq.csv"))
#print(ecsv_file)
catalog = []
#37 2016/12/18 13:21:36.58 23.660 94.314 29.099 M 3.08
for cata in ecsv_file:
    catalog.append(cata)
cat = catalog[37]
year,month,day,hour,minute=cat[0:5]
second=cat[5].split('.')[0]
msec=cat[5].split('.')[1]
evla,evlo,evdp=cat[6:9]
mag=cat[10]
date_str='{}-{}-{}'.format(year,month,day)
date=datetime.datetime.strptime(date_str,'%Y-%m-%d')
days=int(date.strftime("%j"))
print(cat)


os.putenv("SAC_DISPLAY_COPYRIGHT",'0')

#origin = 0
#o = datetime.datetime.strptime(origin,'%Y-%m-&dT%H:%M:%S.%f')
if os.path.exists(template):
    shutil.rmtree(template)
os.makedirs(template)
os.chdir(template)
os.makedirs(os.path.join(year+month+day+hour+minute+second+'.'+msec))
event_path=os.path.join(template,year+month+day+hour+minute+second+'.'+msec)

#-------------------------read trace and change o、header
os.chdir(trace)
s =""

s += "r *.[E,N,Z] \n"
s += "synchronize \n"
s += "ch o gmt {} {} {} {} {} {} \n".format(int(year),days,int(hour),int(minute),int(second),int(msec)*10)
s += "ch allt (0 - &1,o&) iztype IO \n"
s += "ch evlo {} evla {} evdp {} mag {} \n".format(float(evlo),float(evla),float(evdp),float(mag))
s += "cd {} \n".format(event_path)
s += "w over \n"
s += "cut {} {} \n".format(b,a)
s += "r *.[E,N,Z] \n"
s += "w over \n"
s += "q \n"

subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
print("cut finished!")
