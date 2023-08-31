# NIST-SURF-2023-Quantum-Networks
Code and data for my smmer research. 

Explanation of file names:
Names of the data folders:
- I put all the parameters of the data collection on the name of the data folder. It should be self-explanatory by the units which number is bin size, number of bins, number of histograms, integration time, etc. When processing data, ensure that these parameters match the corresponding parameters in the code for data processing. 

In the data folders:
- Time corresponds to the real time of each data point.
- Data corresponds to the full data, in most cases this is a 2d array, where each element is an array representing a histogram.
- Peaks is a 1d array calculated from each histogram in Data.
