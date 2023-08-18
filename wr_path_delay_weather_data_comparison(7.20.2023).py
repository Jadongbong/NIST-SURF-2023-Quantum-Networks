"""
Created some plots with weather data and WR data, specific to the data I was using, not useful. 
"""

import matplotlib.pyplot as plt
import numpy as np
import time
import datetime
import matplotlib.dates as mdates

#College Park Weather Data
college_park_weather_load = np.loadtxt(r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\2023-7-20-11-0-2-CollegePark_fixed.txt', skiprows = 477, usecols = (0, 8))
college_park_weather = np.hsplit(college_park_weather_load, 2)

college_park_time = college_park_weather[0]
college_park_temperature = college_park_weather[1]

college_park_time = college_park_time.flatten()
college_park_time = [datetime.datetime.fromtimestamp(i) for i in college_park_time]
college_park_temperature = college_park_temperature.flatten()

college_park_time = college_park_time[:731]
college_park_temperature = college_park_temperature[:731]

#NIST Weather Data
NIST_weather_load = np.loadtxt(r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\2023-7-20-11-0-2-NIST_fixed.txt', skiprows = 477, usecols = (0, 8))
NIST_weather = np.hsplit(NIST_weather_load, 2)

NIST_time = NIST_weather[0]
NIST_temperature = NIST_weather[1]

NIST_time = NIST_time.flatten()
NIST_time = [datetime.datetime.fromtimestamp(i) for i in NIST_time]
NIST_temperature = NIST_temperature.flatten()

NIST_time = NIST_time[:731]
NIST_temperature = NIST_temperature[:731]

#OTDR Measurements
times = np.load(r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\7.20.2023-7.21.2023(Fiber_End_Reflection_DWDMtoUMD_50ps_8000bins_60s_960hist_609.2us)\Time.npy', allow_pickle = True)
peaks = np.load(r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\7.20.2023-7.21.2023(Fiber_End_Reflection_DWDMtoUMD_50ps_8000bins_60s_960hist_609.2us)\Peaks.npy', allow_pickle = True)
times = times[:730]
peaks = peaks[:730]
times = list(times)
peaks = list(peaks)

#WR Measurements
WRabbit_load = np.loadtxt(r'C:\Users\dnh18\OneDrive - NIST\Documents\JadenHe\NIST_UMD_Connection_LEN_LEN_update_rate_1_2023_07_20_13_06_31.dat', skiprows = 6620, usecols = (0, 9))
WRabbit = np.hsplit(WRabbit_load, 2)

WRabbit_time = WRabbit[0]
WRabbit_time = WRabbit_time.flatten()
WRabbit_time = [i * 0.001 for i in WRabbit_time]
WRabbit_time = [datetime.datetime.fromtimestamp(i) for i in WRabbit_time]
WRabbit_time = WRabbit_time[:43315]

WRabbit_peaks = WRabbit[1]
WRabbit_peaks = WRabbit_peaks.flatten()
WRabbit_peaks = [i - 609200 for i in WRabbit_peaks]
WRabbit_peaks = WRabbit_peaks[:43315]

#Find time stamps in WR data that match with time stamps in OTDR data (not very efficiently written)
WRabbit_new_time = []
WRabbit_new_peaks = []
WRabbit_new_time_length = 0
deleted_items = 0
for i in range(len(times)):
    WRabbit_previous_time_length = WRabbit_new_time_length 
    time1 = times[i - deleted_items]
    for j in range(len(WRabbit_time)):
        WRabbit = WRabbit_time[j]
        if WRabbit.day == time1.day and WRabbit.hour == time1.hour and WRabbit.minute == time1.minute and WRabbit.second == time1.second:
            WRabbit_new_time.append(WRabbit_time[j])
            WRabbit_new_peaks.append(WRabbit_peaks[j])
            WRabbit_new_time_length += 1
    if WRabbit_previous_time_length == WRabbit_new_time_length:
        del times[i - deleted_items]
        del peaks[i - deleted_items]
        deleted_items += 1


difference1 = WRabbit_new_peaks[0] - peaks[0]
WRabbit_new_peaks = [i - difference1 for i in WRabbit_new_peaks]

#Difference
difference = [WRabbit_new_peaks[i] - peaks[i] for i in range(len(peaks))]

print(times[0])
print(WRabbit_new_time[0])

#Plot
fig, ax = plt.subplots(3)
ax[0].plot(NIST_time, NIST_temperature, label = 'NIST Temperature')
ax[0].plot(college_park_time, college_park_temperature, label = 'College Park Temperature')
ax[0].set_title('Weather Data')
ax[0].set_xlabel('Time')
ax[0].set_ylabel('Temperature (C)')
ax[0].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
ax[0].grid()
ax[0].legend()

ax[1].plot(times, peaks, color = 'g', label = 'Fiber End Measurement')
ax[1].plot(WRabbit_new_time, WRabbit_new_peaks, color = 'r', label = 'White Rabbit Measurement')
ax[1].set_title('Fiber End Reflection and WR Measurements')
ax[1].set_xlabel('Time')
ax[1].set_ylabel('Path Delay (ns)')
ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
ax[1].grid()
ax[1].legend()

ax[2].plot(times, difference, color = 'y', label = 'Difference')
ax[2].set_title('Difference in WR Measurement and Fiber End Measurement')
ax[2].set_xlabel('Time')
ax[2].set_ylabel('Time Difference (ns)')
ax[2].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
ax[2].grid()
ax[2].legend()

fig.tight_layout()
plt.show()
