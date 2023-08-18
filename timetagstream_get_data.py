"""
Get time tag stream data
"""

import time
import numpy as np
import TimeTagger

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

#Arbitrary n and integration time
integration_time = 0.01
n = 8

#Initialize
stream = TimeTagger.TimeTagStream(tt, 10**9, [start_channel, click_channel])
channels = [] 
times = []

#Get Data
for i in range(3*(2**n)):
    stream.startFor(integration_time*1e12, clear = True)
    stream.waitUntilFinished()
    buffer = stream.getData()
    channels.append(buffer.getChannels())
    times.append(buffer.getTimestamps())

max_length_channels = max(len(array) for array in channels)
max_length_times = max(len(array) for array in times)

#Pad with zeros to make all arrays the same length to process data easier
channels = [np.pad(array, (0, max_length_channels - len(array)), mode = 'constant') for array in channels]
times = [np.pad(array, (0, max_length_times - len(array)), mode = 'constant') for array in times]

#Save Data
np.save('Channels', channels)
np.save('Times', times)
