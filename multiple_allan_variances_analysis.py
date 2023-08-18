"""
To sample multiple allan deviations throughout the day, no clear pattern. Maybe sample over multiple days and average. 
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates 

def average_peaks(peaks, i):
    if i == 0:
        return peaks
    else:
        new_peaks = [np.average([peaks[2*j + 1], peaks[2*j]]) for j in range(int(len(peaks)/2))]
        if len(new_peaks)*(2**i) > len(peaks):
            return average_peaks(new_peaks, i-1)
        else:
            return new_peaks

def new_average_peaks(peaks, n):
    return [sum(peaks[i:i+n])/n for i in range(0, len(peaks), n) if i+n <= len(peaks)]

def variation(list):
    x = []
    for i in range(len(list)-1):
        x.append((list[i+1] - list[i])**2)
    return np.sqrt(0.5*np.average(x))

data = np.load(r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\7.12.2023-7.13.2023(AllanDeviations_3s_n=8_34times)\Peaks.npy', allow_pickle = True)
start_times = np.load(r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\7.12.2023-7.13.2023(AllanDeviations_3s_n=8_34times)\Times.npy', allow_pickle = True)
integration_time = 3
n = 8
number = 34
minimum_allan_deviations = []

for j in range(34):
    allan_deviations = []
    allan_deviations_new = [] 
    integration_times_new = []
    integration_times = []

    for i in range(1, int(len(data)//3) + 1):
        allan_deviations_new.append(variation(new_average_peaks(data[j], i)))
        integration_times_new.append(integration_time * i)

    for i in range(n+1):
        integration_times.append(integration_time*(2**i))
        allan_deviations.append(variation(average_peaks(data[j], i)))
    
    minimum_allan_deviations.append(min(allan_deviations_new))

fig, ax = plt.subplots()
ax.plot(start_times, minimum_allan_deviations)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
ax.set_title('Minimum Allan Deviations vs. Start Time of Measurement')
ax.set_xlabel('Start Time')
ax.set_ylabel('Minimum Allan Deviation (ns)')
ax.grid()
plt.show()
