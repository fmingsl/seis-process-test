'''
Date: 2022-12-03 16:46:32
LastEditors: FangMing from CUG && fm1790764600@163.com
LastEditTime: 2022-12-16 15:14:44
FilePath: /testdata/travetime.py
'''
import csv
from obspy import geodetics
from obspy.taup import TauPyModel

eventnum=37

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

#-------------------------------------------read event
ecsv_file = csv.reader(open("IBR_eq.csv"))
print(ecsv_file)
catalog = []
#37 2016/12/18 13:21:36.58 23.660 94.314 29.099 M 3.08
for cata in ecsv_file:
    catalog.append(cata)
cat = catalog[eventnum]
elat=float(cat[6])
elon=float(cat[7])
depth=float(cat[8])

#--------------------------------------calculate travetime
pt = []
st = []
for i in range(0,len(sn)):
    #print(sn[i])
    distance = geodetics.gps2dist_azimuth(elat,elon,float(stla[i]),float(stlo[i]))[0]
    angle = geodetics.kilometer2degrees(distance*0.001)
    model = TauPyModel(model="iasp91")
    #pt = model.get_travel_times(depth,angle)
    #print(pt)
    pt.append(model.get_travel_times(depth,angle,phase_list=["ttp"])[0].time)
    st.append(model.get_travel_times(depth,angle,phase_list=["tts"])[0].time)
pt.sort(reverse=True)
st.sort(reverse=True)
print("ttP%s\n" % pt)
print("ttS%s\n" % st)
    