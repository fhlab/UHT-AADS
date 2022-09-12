import numpy as np
from scipy.signal import argrelextrema
import scipy.signal
import pandas as pd
import peakutils.baseline
from matplotlib import pyplot as plt

file = "Insert file"
df = pd.read_csv(file)
df = df[100000:101000]

Time = df["Time"]
Time = Time.to_numpy()
total_time = Time[-1]
total_time_s = total_time / 1000
print("Time interval measured:",np.round(total_time,decimals = 3), "milliseconds")
Voltage = df["Voltage"]
Voltage = Voltage.to_numpy()

baseline = peakutils.baseline(-Voltage)
average_baseline = -np.mean(baseline)
print("Baseline at:", np.round(average_baseline, decimals = 3))

threshold_max_higher_lower_bounds = 10.2
# for local maxima
local_max_higher = argrelextrema(Voltage, np.greater)[0]
local_max_higher = local_max_higher[(Voltage[local_max_higher]>threshold_max_higher_lower_bounds)]
threshold_max_lower_upper_bound = 7
threshold_max_lower_lower_bounds = 2
# for local maxima
local_max_lower = argrelextrema(Voltage, np.greater)[0]
local_max_lower = local_max_lower[(Voltage[local_max_lower]>threshold_max_lower_lower_bounds)]
local_max_lower = local_max_lower[(Voltage[local_max_lower]<threshold_max_lower_upper_bound)]
# for local minima
local_min = argrelextrema(Voltage, np.less)[0]
local_min = local_min[(Voltage[local_min]<8)&(Voltage[local_min]>4)] #change numerical values to match dataset
local_max = np.append(local_max_higher,local_max_lower)

fig = plt.figure(figsize=(8,4))

plt.plot(Time,Voltage)
plt.scatter(Time[local_min],Voltage[local_min],color='gold',s=50,marker='X')
plt.scatter(Time[local_max],Voltage[local_max],color='gold',s=50,marker='X')
fig.suptitle(file, fontsize = 8)
plt.autoscale(enable=True, axis='x', tight=True)
plt.show()
