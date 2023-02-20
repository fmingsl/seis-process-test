'''
Date: 2023-02-18 14:41:33
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2023-02-18 16:01:55
FilePath: /testdata/judgephase.py
'''
import os
import csv
import obspy.taup
from obspy.taup import TauPyModel
from obspy.taup.taup_create import build_taup_model
from obspy.geodetics import locations2degrees

path="/home/cugfm/data/bishe/testdata"
os.chdir(path)
phase="./Txtfile/IBR_new_pha_file"
catalog="./Txtfile/event.csv"
export="./Txtfile/export.txt"
station="./Txtfile/station.csv"
model = TauPyModel(model="iasp91")
tdif=4

# if os.path.exists(export):
#     os.remove(export)

ecsv_file = csv.reader(open(catalog))
scsv_file = csv.reader(open(station))
stat=[]
for s in scsv_file:
    stat.append(s)
phasefile=[]
result=[]
f = open(phase,'r')
for line in f:
    phasefile.append(line)
f.close()

for event in ecsv_file:
    number=event[0]
    lat=event[7]
    lon=event[8]
    dep=event[9]
    wflag = False
    newline = []
    for line in phasefile:
        if "#" in line:
            wflag = False
        if "#" in line and int(number) == int(line.split()[14]):
            wflag = True
            result.append(line)
            continue   #如果要舍弃作判断的那一行，则continue进行下一轮循环
        if wflag == True:
            newline.append(line.split()[0])
    newline=list(set(newline))
    newline.sort()
    for sta in newline:
        for s in stat:
            if sta == s[0]:
                stla=s[1]
                stlo=s[2]
                #stel=s[3]
                break
        dist = locations2degrees(float(lat), float(lon), float(stla), float(stlo))
        arrivals = model.get_travel_times(source_depth_in_km=float(dep), distance_in_degree=dist, phase_list=["P","p","S","s"])
        #print(arrivals)
        pi=0
        si=0
        i=0
        while i<len(arrivals):
            arr = arrivals[i]
            i = i + 1
            if ((arr.name == 'P' or arr.name == 'p') and pi==0) :
                #pname = arr.name
                p_time = arr.time
                pi=1
            if ((arr.name == 'S' or arr.name == 's') and si==0) :
                #sname = arr.name
                s_time = arr.time
                si=1
            if (pi == 1 and si == 1):
                break
        if s_time-p_time <= tdif:
            result.append(sta+' '+'0')
        else:
            result.append(sta+' '+'1')
d=open(export,'w')
for line in result:
    if "#" in line:
        d.write(line)
    else:
        d.write(line+'\n')
d.close()


