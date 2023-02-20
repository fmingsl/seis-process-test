'''
Date: 2022-11-29 15:12:23
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-03 15:01:25
FilePath: /testdata/4-transfer_trace.py
'''
# -*- coding: utf8 -*-
import os
import sys
import glob
import subprocess
import shutil

os.putenv("SAC_DISPLAY_COPYRIGHT", "0")
#---------------------------------------path
path = "/home/cugfm/data/testdata/waveform/" #datapath
pzs="/home/cugfm/data/testdata/PZs/"
trace="/home/cugfm/data/testdata/Trace/"

if os.path.exists(trace):
    shutil.rmtree(trace)
os.makedirs(trace)

#----------------------------remove response
os.chdir(path)
s = ""
for sacfile in glob.glob("*.[E,N,Z]"):
    sta,chn = sacfile.split('.')[0:2]
    pz = glob.glob("{}/SAC_PZs_M1_{}_BH{}_*_*".format(pzs,sta, chn))
    # 暂不考虑多个PZ文件的情况
    if len(pz) != 1:
        sys.exit("PZ file error for {}".format(sacfile))

    s += "r {} \n".format(sacfile)
    s += "rmean; rtr; taper \n"
    s += "trans from pol s {} to none freq 0.01 0.02 10 12\n".format(pz[0])
    s += "mul 1.0e9 \n"
    s += "bp c 2 8 n 4 p 2\n"
    s += "w {}/{} \n".format(trace,sacfile)

s += "q \n"
subprocess.Popen(['sac'], stdin=subprocess.PIPE).communicate(s.encode())
print("----------------------------------------------------------------")
print('finished!')
