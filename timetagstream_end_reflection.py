"""
This code does not work yet, working on fixes, do not use.
"""

import time
import numpy as np
import TimeTagger
import datetime

#Calculate peak of photon counts to get end reflection time
def calculate_peak(timeaxis, histogram_data):
    return sum([timeaxis[j]*histogram_data[j] for j in range(len(histogram_data))])/sum(histogram_data)

#Recursively average every two elements of array based on index i
def exponential_average_peaks(peaks, i):
    if i == 0:
        return peaks
    else:
        new_peaks = [np.average([peaks[2*j + 1], peaks[2*j]]) for j in range(int(len(peaks)/2))]
        if len(new_peaks)*(2**i) > len(peaks):
            return exponential_average_peaks(new_peaks, i-1)
        else:
            return new_peaks

#Linearly average every n elements of array
def linear_average_peaks(peaks, n):
    return [sum(peaks[i:i+n])/n for i in range(0, len(peaks), n) if i+n <= len(peaks)]

#Formula for allan deviation 
def variation(list):
    x = []
    for i in range(len(list)-1):
        x.append((list[i+1] - list[i])**2)
    return np.sqrt(0.5*np.average(x))

def get_linear_allan_deviations(peaks, integration_time):
    integration_times_linear = []
    allan_deviations_linear = []
    for i in range(1, int(len(peaks)//3) + 1):
        integration_times_linear.append(integration_time * i)
        allan_deviations_linear.append(variation(linear_average_peaks(peaks, i)))
    return integration_times_linear, allan_deviations_linear

def get_exponential_allan_deviations(peaks, integration_time, n):
    integration_times_exponential = []
    allan_deviations_exponential = []
    for i in range(n+1):
        integration_times_exponential.append(integration_time*(2**i))
        allan_deviations_exponential.append(variation(exponential_average_peaks(peaks, i)))
    return integration_times_exponential, allan_deviations_exponential

#Binary Search to find times that lie within the specified interval of the end reflection time
def binary_search(array, channel_1_time, end_reflection_time, interval, low, high):
    lower_bound = channel_1_time + end_reflection_time - interval
    upper_bound = channel_1_time + end_reflection_time + interval
    while low <= high:
        mid = (low + high)//2
        if array[mid] >= lower_bound and array[mid] <= upper_bound:
            return mid
        elif array[mid] <= lower_bound:
            low = mid + 1
        else:
            high = mid - 1

#obtain all times of reflections, interval should be less than end reflection time
def get_histogram(channels, times, end_reflection_time, interval):
    indices = np.where(channels == 1)[0]
    histogram_points = []
    length = len(times) - 1
    for index in indices:
        channel_2_index = binary_search(times, times[index], end_reflection_time, interval, index, length)
        if channel_2_index not in indices and channel_2_index != None:
            histogram_points.append(times[channel_2_index] - times[index])
    return histogram_points

#convert reflection times to histogram, can modify the function to specify n_bins rather than binwidth if you wish
def make_histogram(histogram_points, binwidth):
    n_bins = int(np.ceil(np.ptp(histogram_points)/binwidth))
    return np.histogram(histogram_points, n_bins)

#Initialize TimeTagger
tt = TimeTagger.createTimeTagger()
tt.reset()

#Channels
start_channel = 1
click_channel = 2

#Settings
tt.setInputDelay(click_channel, 0)
tt.setInputDelay(start_channel, 0)
tt.setDeadtime(start_channel, 1300)
tt.setDeadtime(click_channel, 1300)
tt.setTriggerLevel(start_channel, 0.5)
tt.setTriggerLevel(click_channel, 0.5)

integration_time = 0.5
number_of_histograms = 5
end_reflection_time = 611921000
interval = 150000

peaks = []
realtimes = []

stream = TimeTagger.TimeTagStream(tt, 10**9, [start_channel, click_channel])
stream.stop()
stream.clear()

for i in range(number_of_histograms):
    stream.startFor(integration_time*1e12, clear = True)
    stream.waitUntilFinished()
    buffer = stream.getData()
    channels = buffer.getChannels()
    times = buffer.getTimestamps()
    realtimes.append(datetime.datetime.now())
    makehistogram = make_histogram(get_histogram(channels, times, end_reflection_time, interval), 50)
    peaks.append(calculate_peak(0.001*makehistogram[1][:-1], makehistogram[0]))

print(peaks)
print(realtimes)
