'''
Date: 2023-02-14 14:50:19
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2023-02-15 11:38:38
FilePath: /bishe/testdata/judgekstnm.py
'''
#判断台站是否与数据台站一致
import os
import glob
from obspy import read
from obspy.io.sac import SACTrace

path="/home/cugfm/data/prodata"
os.chdir(path)

for sn in glob.glob("*"):
    sn_path = os.path.join(path, sn)
    os.chdir(sn_path)
    for yds in glob.glob("201*"):
        yds_path = os.path.join(sn_path, yds)
        os.chdir(yds_path)
        #print(yds_path)
        sacfile=os.listdir(yds_path)
        if len(sacfile)==0:
            continue
        for i in sacfile:
            staname=i.split('.')[0]
            kcm=i.split('.')[1]    
            sac = SACTrace.read(i,headonly=True)
            if sn != sac.kstnm:
                #sac.kstnm=sn
                #sac.write(i,headonly=True)
                print("%s!=%s %s" % (sn,sac.kstnm,yds))                                
 