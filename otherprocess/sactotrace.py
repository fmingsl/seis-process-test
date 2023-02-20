'''
Date: 2023-02-15 17:07:19
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2023-02-17 10:21:13
FilePath: /bishe/testdata/sactotrace.py
'''
#去仪器相应，写入台站经纬度信息
import os
import glob
import csv
from obspy import read
from obspy.io.sac import SACTrace
import subprocess

os.putenv("SAC_DISPLAY_COPYRIGHT", "0")
path="/home/cugfm/data/bishe/testdata"
os.chdir(path)
data_path="/home/cugfm/data/prodata"
#data_path="/home/cugfm/data/bishe/testdata/test"
save_path="/home/cugfm/data/trace"
station="/home/cugfm/data/bishe/testdata/Txtfile/station.csv"
pzs="/home/cugfm/data/bishe/testdata/PZs"


#----------------------------read sta_data
scsv_file = csv.reader(open(station))
staname=[]
stla=[]
stlo=[]
stel=[]
for s in scsv_file:
    staname.append(s[0])
    stla.append(float(s[1]))
    stlo.append(float(s[2]))
    stel.append(float(s[3]))

os.chdir(data_path)
for sn in glob.glob("E*"):
    sn_path = os.path.join(data_path, sn)
    os.chdir(sn_path)
    for yds in glob.glob("201*"):
        yds_path=os.path.join(sn_path,yds)
        save_path1=os.path.join(save_path,sn,yds)
        if os.path.exists(save_path1):
            print(sn,yds,"has already trans")
            continue
        sacfile=os.listdir(yds_path)
        if len(sacfile)==0:
            continue
        os.makedirs(save_path1)
        os.chdir(yds_path)
        s=""
        for sf in sacfile:
            kcm=sf.split('.')[1]
            #写入台站经纬度
            sac=SACTrace.read(sf,headonly=True)
            for j in range(0,len(staname)):
                if staname[j]==sn:
                    sac.stla=stla[j]
                    sac.stlo=stlo[j]
                    sac.stel=stel[j]
                    sac.lcalda=1
                    sac.kcmpnm=kcm
                    sac.write(sf,headonly=True)
                    break
            
            #去仪器响应
            pz = glob.glob("{}/SAC_PZs_M1_{}_BH{}_*_*".format(pzs,sn,kcm))
            if len(pz)!=1:
                for i in pz:
                    pzname=i.split('/')[-1]
                    time=pzname.split('__')[1]
                    btime=time.split('_')[0].split('.')[0:2]
                    etime=time.split('_')[1].split('.')[0:2]
                    bt=btime[0]+btime[1]
                    et=etime[0]+etime[1]
                    if yds > bt and yds < et:
                        pz[0]=i
                        break
            s += "r {} \n".format(sf)
            s += "rmean; rtr; taper \n"
            s += "trans from pol s {} to none freq 0.01 0.02 10 12\n".format(pz[0])
            s += "mul 1.0e9 \n"
            s += "bp c 2 8 n 4 p 2\n"
            s += "w {}/{} \n".format(save_path1,sf) 
        s += "q \n"
        subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
        print(sn,yds,'has trans')            
            
                
            



