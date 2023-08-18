"""
Calculate Allan deviations
"""

import numpy as np
import matplotlib.pyplot as plt

data = np.load(r'') #path for peaks calculatd from get_data file 

def exponential_average(peaks, i):
    if i == 0:
        return peaks
    else:
        new_peaks = [np.average([peaks[2*j + 1], peaks[2*j]]) for j in range(int(len(peaks)/2))]
        if len(new_peaks)*(2**i) > len(peaks):
            return exponential_average(new_peaks, i-1)
        else:
            return new_peaks

def linear_average(peaks, n):
    return [sum(peaks[i:i+n])/n for i in range(0, len(peaks), n) if i+n <= len(peaks)]

def variation(list):
    x = []
    for i in range(len(list)-1):
        x.append((list[i+1] - list[i])**2)
    return np.sqrt(0.5*np.average(x))

integration_time = 30 #Copied over from get_data file
n = 5 #Copied over from get_data file

exponential_allan_deviations = []
exponential_integration_times = []

linear_allan_deviations= [] 
linear_integration_times = []

for i in range(n+1):
    exponential_integration_times.append(integration_time*(2**i))
    exponential_allan_deviations.append(variation(exponential_average(data, i)))

for i in range(1, int(len(data)//3) + 1):
    linear_integration_times.append(integration_time * i)
    linear_allan_deviations.append(variation(linear_average(data, i)))

#Plot
fix, ax = plt.subplots()
ax.plot(exponential_integration_times, exponential_allan_deviations, label = "Exponential Method")
ax.plot(linear_integration_times, linear_allan_deviations, label = "Linear Method")
ax.set_xlabel("Integration Time (s)")
ax.set_ylabel("Allan Deviation (ns)")
ax.set_title("Allan Deviation vs. Integration Time")
ax.legend()
ax.grid() 
plt.show()
