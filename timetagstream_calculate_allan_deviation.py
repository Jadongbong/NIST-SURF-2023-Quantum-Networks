"""
Calculate allan deviations from time tag stream
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

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
    length = len(times) - 1 #-1 is necessary due to array indexing starting at 0
    for index in indices:
        channel_2_index = binary_search(times, times[index], end_reflection_time, interval, index, length)
        if channel_2_index not in indices and channel_2_index != None:
            histogram_points.append(times[channel_2_index] - times[index])
    return histogram_points

#convert reflection times to histogram, can modify the function to specify n_bins rather than binwidth if you wish
def make_histogram(histogram_points, binwidth):
    n_bins = int(np.ceil(np.ptp(histogram_points)/binwidth))
    return np.histogram(histogram_points, n_bins)

#Load in data
channels = np.load('Channels.npy', allow_pickle = True)
times = np.load('Times.npy', allow_pickle = True)

#Set paramters
end_reflection_time = 611921000 #As accurate as possible
interval = 100000

#Arbitrary n and integration time, match with timetagstream_get_data
n = 8
integration_time = 0.01

#Get Peaks
peaks = []
for i in range(len(times)):
    histogram_points = get_histogram(channels[i], times[i], end_reflection_time, interval)
    makehistogram = make_histogram(histogram_points, 50)
    timeaxis = 0.001*makehistogram[1][:-1] #0.001 to convert to nanoseconds
    histogram = makehistogram[0]
    peaks.append(calculate_peak(timeaxis, histogram))

#Get Allan Deviations
integration_times_exponential = get_exponential_allan_deviations(peaks, integration_time, n)[0]
allan_deviations_exponential = get_exponential_allan_deviations(peaks, integration_time, n)[1]
integration_times_linear = get_linear_allan_deviations(peaks, integration_time)[0]
allan_deviations_linear = get_linear_allan_deviations(peaks, integration_time)[1]

#Plot
fix, ax = plt.subplots()
ax.plot(integration_times_exponential, allan_deviations_exponential, label = "Exponential Method")
ax.plot(integration_times_linear, allan_deviations_linear, label = "Linear Method")
ax.set_xlabel("Integration Time (s)")
ax.set_ylabel("Allan Deviation (ns)")
ax.set_title("Allan Deviation vs. Integration Time")
ax.legend()
ax.grid() 
plt.show()

#Make histogram, to test if get_histogram and make_histogram are working properly 
"""histogram_points = get_histogram(channels, times, end_reflection_time, interval)
make_histogram = make_histogram(histogram_points, 50)

timeaxis = 0.000001*make_histogram[1][:-1] #remove last item from timeaxis array since size of bin edges array is one more than size of histogram array, 0.000001 factor to convert to microseconds
histogram = make_histogram[0]"""

#Plot
"""fig, ax = plt.subplots()
ax.plot(timeaxis, histogram)
ax.grid()
ax.set_xlabel('Reflection Time (ns)')
ax.set_ylabel('Number of Counts')
ax.set_title('Histogram of Photon Counts vs. Time')
plt.show()"""

#To compare speed of regular 'for' loop to binary search

#For Loop
"""for i in np.where(channels == 1)[0]:
    channel_1_time = times[i]
    for j in times:
        if j >= channel_1_time + end_reflection_time - interval and j <= channel_1_time + end_reflection_time + interval:
            print(j)"""

#Binary Search
"""for i in np.where(channels == 1)[0]:
    channel_1_time = times[i]
    index = binary_search(times, channel_1_time, end_reflection_time, interval, 0, length)
    if index != None:
        print(times[index])"""
