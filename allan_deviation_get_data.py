# -*- coding: utf-8 -*-
"""
Get data from TimeTagger
"""

import numpy as np
import matplotlib.pyplot as plt
import TimeTagger 
import time
import datetime

#Calculate peak of photon counts to get end reflection time
def calculate_peak(timeaxis, histogram_data):
    return sum([timeaxis[j]*histogram_data[j] for j in range(len(histogram_data))])/sum(histogram_data)

tt = TimeTagger.createTimeTagger()

#Channels
start_channel = 1
click_channel = 2
tt.reset()

#Bins
binwidth = 50
n_bins = 5000
timeaxis = [i*binwidth*0.001 for i in range(n_bins)] #Time axis in nanoseconds

#Settings
tt.setInputDelay(click_channel, 0)
tt.setInputDelay(start_channel, 611800000) #Manually set delay
tt.setDeadtime(start_channel, 1300)
tt.setDeadtime(click_channel, 1300)
tt.setTriggerLevel(start_channel, 0.5)
tt.setTriggerLevel(click_channel, 0.5)

#Arbitrary n and integration time
integration_time = 1
n = 10

#Initialize
histogram = TimeTagger.Histogram(tt, click_channel, start_channel, binwidth, n_bins)
histogram.stop()
histogram.clear()
time.sleep(1)

peaks = []
histogram_data = []

#Data Collection
for i in range(3*(2**n)): #Total amount of data points is 3 * 2^n, so when average data points recursively, there are 3 data points left after the final averaging
    histogram.startFor(integration_time*1e12, clear = True)
    histogram.waitUntilFinished()
    h = histogram.getData()
    histogram_data.append(h) 
    print(sum(h)) #To make sure detector did not go normal, not necessary
    peaks.append(calculate_peak(timeaxis, h))

#Save Data
np.save("Peaks", peaks) #Important, what should be loaded into process_data file
np.save("Data", histogram_data) #Raw Data, not necessary

#Final
TimeTagger.freeTimeTagger(tt)
