'''
Date: 2022-12-01 18:40:52
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-16 15:21:29
FilePath: /testdata/chkztime.py
'''
import os
import sys
import glob
import subprocess
from obspy import read
#from obspy.core import UTCDateTime

os.putenv("SAC_DISPLAY_COPYRIGHT", "0")
#---------------------------------------path
path="/home/cugfm/data/testdata/Trace/"

#----------------------------change kztime and b
os.chdir(path)
s = ""
for sacfile in glob.glob("*.[E,N,Z]"):
    st = read(sacfile)
    date=st[0].stats.starttime
    msec=date.microsecond
    ms=msec/1000000
    if msec < 100000: 
        s += "r {} \n".format(sacfile)
        s += "ch nzmsec 0 \n"
        s += "ch b {} \n".format(ms)
        s += "w over \n"
        s += "cuterr fillz;cut 0 e \n"
        s += "r {} \n".format(sacfile)
        s += "w over \n" 
    else:
        print("msec of %s is over 0.1sec!!!" % sacfile)
        continue


s += "q \n"    
                   
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
print("----------------------------------------------------------------")
print('change finished!')