import pandas as pd
import peakutils.baseline
from matplotlib import pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.signal
import numpy as np


droplet_threshold = 9.9 #adjust to desired threshold
hits_threshold = 9.7 #adjust to desired threshold
distance_between_peaks = 20 # number of samples between neighbouring peaks
relative_height = 0.5 # the relative height at which peak width is measured, e.g. 0.5 is at half the prominence height
sample_rate = 263.000000/9994  #sample rate of detector
bins = 100 # number of histogram bins
residence_time_low = 0.1 #minimum residence time for gating in microseconds
residence_time_high = 0.3 #maximum residence time for gating in microseconds

file = "INSERT FILE" # file should be a csv with a “Time” column and a “Voltage” column with headers
df = pd.read_csv(file)
df = df[5000:6000] # select data range or comment out to use all data

#convert to pandas dataframe
Time = df["Time"]
Time = Time.to_numpy()
total_time = Time[-1]
total_time_s = total_time / 1000
print("Time interval measured:",np.round(total_time,decimals = 3), "milliseconds")
Voltage = df["Voltage"]
Voltage = Voltage.to_numpy()

#baseline detection
baseline = peakutils.baseline(-Voltage)
average_baseline = -np.mean(baseline)
print("Baseline at:", np.round(average_baseline, decimals = 3))

#peak detection
minima_V = Voltage*-1
minima = scipy.signal.find_peaks(minima_V,distance=distance_between_peaks,height=-droplet_threshold)
minima_sort = scipy.signal.find_peaks(minima_V,distance=distance_between_peaks,height=(-hits_threshold,-9.25))
points, _ = minima
points_sort, _ = minima_sort
min_pos = Time[minima[0]]
min_height = minima_V[minima[0]]
peak_widths = scipy.signal.peak_widths(minima_V,points, rel_height=relative_height)
widths = peak_widths[0]
residence_time = widths*sample_rate

#graphs without gating

gs = gridspec.GridSpec(2,2, wspace = 0.5, hspace = 0.5, top = 0.94)

#voltage against time
fig = plt.figure()
ax1 = fig.add_subplot(gs[1,:])
ax1.plot(Time,Voltage)
ax1.scatter(min_pos,min_height*-1,color='gold',s=50,marker='X')
plt.xlabel("Time [ms]")
plt.ylabel("Detection Signal [V]")
ax1.grid()

#voltage against residence time
ax2 = fig.add_subplot(gs[0,1])
plt.scatter(residence_time,Voltage[points], alpha=0.1)
plt.xlabel("Residence time [us]")
plt.ylabel("Voltage [V]")

#histogram of droplet detection signals [V]
ax3 = fig.add_subplot(gs[0,0])
plt.hist(min_height*-1,bins=bins)
plt.xlabel("Detection signal [V]")
plt.ylabel("Relative frequency")
fig.suptitle(file, fontsize = 8)
plt.show()

#printing of detected data
frequency = points.size/total_time_s
print(np.around(frequency,decimals = 1),"droplets per second")
print(points.size, "droplets detected")
print(points_sort.size,"droplets detected above threshold")
V_values_above_threshold = Voltage[points_sort[:99]]
print("Standard deviation of droplet voltages detected above threshold:",np.round(np.std(V_values_above_threshold), decimals = 3), "volts")

#peak detection for gating and printing of detected data
peak_widths = scipy.signal.peak_widths(minima_V,points_sort, rel_height=relative_height)
widths = peak_widths[0]
residence_time = widths*sample_rate
residence_time_gated = residence_time > residence_time_low
residence_time_gated = residence_time[np.where((residence_time >= residence_time_low) & (residence_time <= residence_time_high))]
points1 = points_sort[np.where((residence_time > residence_time_low) & (residence_time < residence_time_high))]
gated_voltage = Voltage[points1]
print(len(residence_time_gated),"droplets detected with gate")

#graphs with gating

#gated histogram of droplet detection signals
gs = gridspec.GridSpec(1,2, wspace = 0.5, hspace = 0.5, top = 0.94)
fig = plt.figure()
ax4 = fig.add_subplot(gs[:,1])
plt.hist(gated_voltage,bins=bins)
plt.xlabel("Detection signal [V]")
plt.ylabel("Relative frequency")
plt.title("Voltage with Gated Residence Time")

#gated voltage against residence time
ax4 = fig.add_subplot(gs[0,0])
plt.scatter(residence_time_gated,gated_voltage, alpha=0.5)
plt.xlabel("Residence time [us]")
plt.ylabel("Voltage [V]")
plt.title("Gated Residence Time")
plt.show()
