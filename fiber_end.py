# -*- coding: utf-8 -*-
"""
Fiber End reflection time throughout the day.
"""

import numpy as np
import matplotlib.pyplot as plt
import TimeTagger 
import time
import datetime
import matplotlib.dates as mdates

#Calculate Peak Function
def calculate_peak(timeaxis, histogram_data):
    return sum([timeaxis[j]*histogram_data[j] for j in range(len(histogram_data))])/sum(histogram_data)

#Create
tt = TimeTagger.createTimeTagger()
tt.reset()

#Channels
start_channel = 1
click_channel = 2

#Time
integration_time = 0.5 #Arbirary integration time, ideally should be time with the lowest allan deviation
number_of_histograms = 172800 #integratoin_time * number_of_histograms = time to take data
rest_time = 0.001 #probably can get rid of this

#New bins and settings
binwidth = 50
n_bins = 8000

timeaxis = [i*binwidth*0.001 for i in range(n_bins)] #Time axis in nanoseconds

#Settings
tt.setInputDelay(click_channel, 0)
tt.setInputDelay(start_channel, 611750000) #Manually set delay 
tt.setDeadtime(start_channel, 1300)
tt.setDeadtime(click_channel, 1300)
tt.setTriggerLevel(start_channel, 0.5)
tt.setTriggerLevel(click_channel, 0.5)

#Initialization
histogram = TimeTagger.Histogram(tt, click_channel, start_channel, binwidth, n_bins)
peaks = []
realtime = []

#Data Collection
for i in range(number_of_histograms):
    histogram.startFor(integration_time*1e12, clear = True)
    histogram.waitUntilFinished()
    h = histogram.getData()
    print(sum(h)) #To make sure that the detector did not go normal, not necessary
    realtime.append(datetime.datetime.now())  
    peaks.append(calculate_peak(timeaxis, h))
    time.sleep(rest_time) #Probably not necessary 

#Save
np.save("Peaks", peaks) #End reflection time
np.save("Time", realtime) #Actual time in EST of each peak 

#Plot
fig, ax = plt.subplots()
ax.plot(realtime, peaks)
ax.set_xlabel("Time")
ax.set_ylabel("Fiber End Reflection (ns)")
ax.set_title("7/27/2023-7/28/2023 Fiber End Reflection Time")
ax.grid()
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
plt.show()

TimeTagger.freeTimeTagger(tt)
