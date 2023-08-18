"""
Quick code to save times and data to matlab file to plot 3d 
"""

import scipy as sci
import numpy as np 
import time
import datetime


Data = np.load('Data.npy', allow_pickle=True)
#unixtime = [time.mktime(i.timetuple()) for i in Time]

sci.io.savemat('Data(UMD)(2).mat', {'Data': Data})
