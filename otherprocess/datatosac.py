'''
Date: 2023-02-14 20:17:57
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2023-02-15 08:59:08
FilePath: /bishe/testdata/datatosac.py
'''
#将原始文件转化为sac
import os
import glob
import shutil
from obspy import read

path="/home/cugfm/data/bishe/testdata"
os.chdir(path)
data_path="/home/cugfm/data/CMGSMO-P1/data"
save_path="/home/cugfm/data/prodata"
dss="/home/cugfm/data/bishe/testdata/Txtfile/daymissing.txt"
daymissing=[]
f=open(dss,"r")
for line in f:
    daymissing.append(line.strip())
f.close()

#清空注意！！！
# if os.path.exists(save_path):
#     shutil.rmtree(save_path)
# os.makedirs(save_path)
os.chdir(data_path)
for sn in glob.glob("M3*"):
    sn_path=os.path.join(data_path,sn)
    for yds_path in glob.glob(sn_path+"/201*"):
        yds=yds_path.split("/")[-1]
        save_path1=os.path.join(save_path,sn,yds)
        if os.path.exists(save_path1):
            print(sn,yds,"has already trans")
            continue
        os.makedirs(save_path1)
        #有点问题，未测试---
        wflag=False
        for i in daymissing:
            if i == sn+'	'+yds:
                wflag=True
                break
        if wflag==True:
            continue
        #---------------
        os.chdir(yds_path)
        j=glob.glob("9*")[0]
        filedir_path=os.path.join(yds_path,j,'1')
        os.chdir(filedir_path)
        reftek_file=os.listdir(filedir_path)
        st = read(reftek_file[0],format='REFTEK130',component_codes='ZNE')
        st.clear()
        for f in reftek_file:
            st += read(f,format='REFTEK130',component_codes='ZNE')                
        st.sort(['starttime'])
        st.merge(method=1,fill_value=0)
        st[0].write(os.path.join(save_path1,sn+'.E'),format='SAC')
        st[1].write(os.path.join(save_path1,sn+'.N'),format='SAC')
        st[2].write(os.path.join(save_path1,sn+'.Z'),format='SAC')
        print(sn,yds,"has trans to sac")    
