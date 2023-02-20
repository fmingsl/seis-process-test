'''
Date: 2023-02-15 18:59:00
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2023-02-15 18:59:09
FilePath: /bishe/testdata/mulpz.py
'''
#考虑有多个仪器响应文件的情况
import os
import sys
import glob
import subprocess
import shutil
import datetime

os.putenv("SAC_DISPLAY_COPYRIGHT", "0")

path="/home/cugfm/data/bishe/testdata/test"
os.chdir(path)
pzs="/home/cugfm/data/bishe/testdata/PZs"
save_path="/home/cugfm/data/bishe/testdata/test/M070"

for sn in glob.glob("*"):
    sn_path = os.path.join(path, sn)
    os.chdir(sn_path)
    for yds in glob.glob("201*"):
        yds_path = os.path.join(sn_path, yds)
        os.chdir(yds_path)
        s=""
        for sacfile in glob.glob("*.[E,N,Z]"):
            sta,chn=sacfile.split('.')[0:2]
            pz = glob.glob("{}/SAC_PZs_M1_{}_BH{}_*_*".format(pzs,sta, chn))
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
            s += "r {} \n".format(sacfile)
            s += "rmean; rtr; taper \n"
            s += "trans from pol s {} to none freq 0.01 0.02 10 12\n".format(pz[0])
            s += "mul 1.0e9 \n"
            s += "bp c 2 8 n 4 p 2\n"
            s += "w {}/{} \n".format(save_path,sacfile) 
        s += "q \n"
        subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
        print(sn,yds,'has trans')                       
            
                    