'''
Date: 2022-11-28 13:21:59
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-03 14:44:38
FilePath: /testdata/3-process.py
'''
import os,csv
#from obspy import read
from obspy.io.sac import SACTrace
#import shutil,glob

path="/home/cugfm/data/testdata"
os.chdir(path)
#data_path="/home/cugfm/data/testdata/data"
waveform="/home/cugfm/data/testdata/waveform/"
#pzs="/home/cugfm/data/testdata/PZs"

class trace:
    sn=[]
    stla=[]
    stlo=[]
    stel=[]

#----------------------------read sta_data
scsv_file = csv.reader(open("selectsta.csv"))
for s in scsv_file:
    trace.sn.append(s[0])
    trace.stla.append(float(s[1]))
    trace.stlo.append(float(s[2]))
    trace.stel.append(float(s[3]))

# print(trace.sn)
# print(trace.stla)
os.chdir(waveform)

sacfile = os.listdir(waveform)
print(sacfile)
for i in sacfile:
    #print(i)
    staname=i.split('.')[0]
    kcm=i.split('.')[1]
    #st = read(i)
    sac = SACTrace.read(i,headonly=True)
    #print(st)
    for j in range(0,len(trace.sn)):
        if staname == trace.sn[j]:
            #header={'stla':trace.stla[j],'stlo':trace.stlo[j],'stel':trace.stel[j],'lcalda':1,'kcmpnm':kcm}
            #st = SACTrace(**header)
            #st = SACTrace(stla=trace.stla[j],stlo=trace.stlo[j],stel=trace.stel[j],lcalda=1,kcmpnm=kcm)        
            #tr = []
            #tr = st[0]
            #print(st)
            #print(tr.stats)
            #print('j=%s' % j)
            #print('staname=%s' % staname)
            sac.stla=trace.stla[j]
            sac.stlo=trace.stlo[j]
            sac.stel=trace.stel[j]
            sac.lcalda=1
            sac.kcmpnm=kcm
            sac.write(i,headonly=True)
            print("---------------------------------\n")
            print("%s\n" % sac)
        else:
            continue
        
            


