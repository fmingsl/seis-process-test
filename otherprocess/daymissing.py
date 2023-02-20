'''
Date: 2023-02-14 09:02:14
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2023-02-14 18:33:19
FilePath: /bishe/testdata/daymissing.py
'''
#找出存在缺失的数据所在的天数
import os
import glob
import numpy as np
path="/home/cugfm/data/bishe/testdata"
os.chdir(path)
data_path="/home/cugfm/data/CMGSMO-P1/data"
os.chdir(data_path)
dss="/home/cugfm/data/bishe/testdata/Txtfile/daymissing.txt"
daymissing=[]
for sn in glob.glob("*"):
    sn_path=os.path.join(data_path,sn)
    for yds_path in glob.glob(sn_path+"/201*"):
        yds=yds_path.split("/")[-1]
        j=glob.glob(yds_path+"/9*")
        if len(j)!=1:
            print("Error %s !=1" % j)
            daymissing.append(sn+"	"+yds)
            continue
        j=j[0]
        dpath2=os.path.join(j,'1')
        if os.path.exists(dpath2):
            os.chdir(dpath2)
        else:
            print("目录不存在,%s %s" % (sn,yds))
            daymissing.append(sn+"	"+yds)
            continue        
        reftek_file = os.listdir(dpath2)
        if len(reftek_file)!=24:
            print("Error %s!=24" % len(reftek_file))
            daymissing.append(sn+"	"+yds)
            continue
        time=[]
        wflag=False
        for i in reftek_file:
            time.append(i[0:2])
            mins=i[2:6]
            if int(mins) != 0:
                wflag=True
                print("mins = %s" % mins)
                break
        if wflag==True:
            daymissing.append(sn+"	"+yds)
            continue        
        if len(set(time))!=24:
            print("Error %s!=24" % len(set(time)))
            daymissing.append(sn+"	"+yds)
            continue
        
d=open(dss,'w')
daymissing.sort()
for i in daymissing:
    d.write(i+"\n")
d.close()    
        
    

        