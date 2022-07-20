import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import os
import Lab3Functions as l3f
import emgfuction as emgf

path = '/Users/sengunoglud/Desktop/Movement1'
i = 0
for filename in os.listdir(path):
    os.rename(os.path.join(path,filename), os.path.join(path,'obs'+str(i)+'.csv'))
    i = i +1

column_names = [
    "t",
    "v"
]
mv = l3f.import_data(",")
print(mv)
#plt.plot(mv.t,mv.v)

time = mv.t
emg = mv.v

emg_correctmean =emgf.remove_mean(emg, time)
#plt.show()

emg_filtered = emgf.emg_filter(emg_correctmean,time)
#plt.show()

emg_rectified = emgf.emg_rectify(emg_filtered,time)
#plt.show()

emgf.allinone(time, emg_correctmean,low_pass=0.05,sfreq=1000,high_band=20, low_band=450)
plt.show()


