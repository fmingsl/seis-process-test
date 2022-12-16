'''
Date: 2022-12-04 19:35:58
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-05 19:33:49
FilePath: /testdata/determine_eventselectsta_days.py
'''
# %%
#判断这些台站是否有事件的数据
import os,csv,glob,sys
import datetime
from obspy import geodetics

path="/home/cugfm/data/testdata"
data_path="/home/cugfm/data/CMGSMO-P1/data"
os.chdir(path)

#-----------------------------------read event
ecsv_file = csv.reader(open("IBR_eq.csv"))
catalog = []
#37 2016/12/18 13:21:36.58 23.660 94.314 29.099 M 3.08
for cata in ecsv_file:
    catalog.append(cata)
cat = catalog[15]
year=cat[0]
month=cat[1]
day=cat[2]
print(cat)
date_str='{}-{}-{}'.format(year,month,day)
date=datetime.datetime.strptime(date_str,'%Y-%m-%d')
days=date.strftime("%j")
yd=year+days

#----------------------------read sta_data
scsv_file = csv.reader(open("selectsta.csv"))
#print(scsv_file)
sn = []
stla = []
stlo = []
stel = []
#37 2016/12/18 13:21:36.58 23.660 94.314 29.099 M 3.08
for s in scsv_file:
    sn.append(s[0])
    stla.append(s[1])
    stlo.append(s[2])
    stel.append(s[3])

print(sn)

for i in range(0,len(sn)):
        dpath1 = os.path.join(data_path,sn[i],yd)
        if os.path.exists(dpath1):
            os.chdir(dpath1)
        else:
            print("目录不存在,data_path:%s"% dpath1)
            continue
        j=glob.glob('9*')[0]
        dpath2 = os.path.join(dpath1,j,'1')    
        if os.path.exists(dpath2):
            pass
        else:
            print("目录不存在,data_path:%s,sn:%s,day:%s" % data_path,sn[i],yd)
            continue
        print(dpath2)
        


