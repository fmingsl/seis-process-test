'''
Date: 2023-02-14 20:56:09
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2023-02-16 16:08:57
FilePath: /bishe/testdata/dmdatatosac.py
'''
#dmdatatosac.copy()
import os
import glob
import shutil
from obspy import read

path="/home/cugfm/data/bishe/testdata"
os.chdir(path)
data_path="/home/cugfm/data/CMGSMO-P1/data"
save_path="/home/cugfm/data/dmprodata"
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
for sn_yds in daymissing:
    sn=sn_yds.split()[0]
    yds=sn_yds.split()[1]
    save_path1=os.path.join(save_path,sn,yds)
    if os.path.exists(save_path1):
        print(sn,yds,"has already trans")
        continue
    yds_path=os.path.join(data_path,sn,yds)
    os.chdir(yds_path)
    j=glob.glob("9*")
    # if len(j)!=1:
    #     print(sn,yds,"9*dir !=1")
    #     continue
    filedir_path=os.path.join(yds_path,j[0],'1/')
    if os.path.exists(filedir_path):
        os.chdir(filedir_path)
    else:
        print(sn,yds,"has no 1")
        continue
    reftek_file=os.listdir(filedir_path)
    # if len(reftek_file)==0:
    #     print(sn,yds,"has no reftekdata")
    #     continue
    os.makedirs(save_path1)   
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
    

    
 