'''
Date: 2022-11-16 16:15:26
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-11-16 16:17:28
FilePath: /Desktop/1/readdata.py
'''
from obspy import read
import os
import glob
import shutil

#path = "/home/cugfm/Desktop/1/Rawdata"

os.getcwd() #查看当前工作路径
#os.chdir(path) #更改当前路径

st = read("N03.E")
tr = st[0]
print(tr)
print(tr.stats)

    #sactr = read(tr[0])

#print(sactr)
#print(sactr.stats)
#print(st)
#len(st)
#print(st.stats.reftek130)
#tr = st[0]

#print(tr)
#print(tr.stats)

#print(tr.stats.reftek130.position)

    
