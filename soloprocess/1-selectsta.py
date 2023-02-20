'''
Date: 2022-11-23 19:15:45
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-15 18:58:02
FilePath: /testdata/1-selectsta.py
'''
import os,csv
from obspy import geodetics

path="/home/cugfm/data/testdata"
os.chdir(path)

ecsv_file = csv.reader(open("IBR_eq.csv"))
#fd = open("IBR_eq.csv","r",encoding="utf-8")
print(ecsv_file)
catalog = []
#37 2016/12/18 13:21:36.58 23.660 94.314 29.099 M 3.08
for cata in ecsv_file:
    catalog.append(cata)
#for i in range(0,len(catalog)):
cat = catalog[37]
#print(catalog)
elat=float(cat[6])
elon=float(cat[7])
print(elat,"\n",elon)
print(cat)

scsv_file = csv.reader(open("station.csv"))
print(scsv_file)
sta=[]
for s in scsv_file:
    print(s)
    sname=s[0]
    slat=float(s[1])
    slon=float(s[2])
    distance = geodetics.gps2dist_azimuth(elat,elon,slat,slon)[0]
    angle = geodetics.kilometer2degrees(distance*0.001)
    if(angle < 1):
        sta.append(s)
    else: 
        continue
    print(sname)
    
csvFile = open('selectsta.csv','w',newline='')
with csvFile:
    writer = csv.writer(csvFile)
    writer.writerows(sta)

        
'''
for line in fd.readlines():
    line = line.strip()
    catalog = line.append()
    #print(":%s" %(line))
'''
#print(line)
#print(catalog)
#line = fd.readlines()
#ma = []
#print(line)
#print(ma[0:5])
#fd.close()
