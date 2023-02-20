'''
Date: 2022-11-29 15:37:42
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-03 15:01:12
FilePath: /testdata/clear pz_*.py
'''
import os
import glob

path = '/home/cugfm/data/testdata/PZs/'
os.chdir(path)
for file in glob.glob("SAC_PZs_M1*"):
    with open(file,mode='r',encoding="utf-8") as f:
        lines = f.readlines()
    ge = ['*']
    new = ''
    for line in lines:
        mode = True
        for i in ge:
            if i in line:
                mode = False
                break
        if mode:
            new += line
    with open(file,'w') as f:
        f.write(new)
print("clear complete!")        
