'''
Date: 2022-11-24 10:30:46
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-15 18:59:20
FilePath: /testdata/2-statowave.py
'''
import os,csv,sys
from obspy import read
import shutil,glob
import datetime
# import matplotlib.pyplot as plt

path="/home/cugfm/data/testdata"
os.chdir(path)
data_path="/home/cugfm/data/CMGSMO-P1/data"
waveform="/home/cugfm/data/testdata/waveform/"

#-----------------------------------read event
ecsv_file = csv.reader(open("IBR_eq.csv"))
#print(ecsv_file)
catalog = []
#37 2016/12/18 13:21:36.58 23.660 94.314 29.099 M 3.08
for cata in ecsv_file:
    catalog.append(cata)
cat = catalog[37]
year=cat[0]
month=cat[1]
day=cat[2]
print(cat)

#------------------------------------月日转天数
'''
def today(n):
    if n % 4 == 0 and n % 100 != 0 or n %400 == 0:
        return True
    else:
        return False
    
date = [year,month,day] 
month_day=[0,31,0,31,30,31,30,31,31,30,31,30,31]
if today(date[0]):
    month_day[2] = 29
else:
    month_day[2] = 28
day_sum = 0
for i in range(1,date[1]):
    day_sum += month_day[i]
day_sum += date[2]
days = str(date[0]) + str(day_sum)
print(tds)
#print("%d" % day_sum)
'''
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

#--------------------------------------find and merge data from station    
def sta_data(sn,day,data_path,save_path):
    for i in range(0,len(sn)):
        dpath1 = os.path.join(data_path,sn[i],day)
        if os.path.exists(dpath1):
            os.chdir(dpath1)
        else:
            print("目录不存在,data_path:%s"% dpath1)
            continue
        j=glob.glob('9*')[0]
        dpath2 = os.path.join(dpath1,j,'1')    
        if os.path.exists(dpath2):
            os.chdir(dpath2)
        else:
            print("目录不存在,data_path:%s,sn:%s,day:%s" % data_path,sn[i],day)
            continue
        os.chdir(dpath2)
        reftek_file = os.listdir(dpath2)
        st = read("00*")
        st.clear()
        for f in reftek_file:
            st += read(f)
        st.sort(['starttime'])    
        st.merge(method=1)           
        st[0].write(os.path.join(save_path,sn[i]+'.N'),format='SAC')
        st[1].write(os.path.join(save_path,sn[i]+'.E'),format='SAC')
        st[2].write(os.path.join(save_path,sn[i]+'.Z'),format='SAC')
        print("%s which trans to sac is complete!" % sn[i])     
      
save_path=waveform
if os.path.exists(save_path):
    shutil.rmtree(save_path)
os.makedirs(save_path)
        
sta_data(sn,yd,data_path,save_path)
