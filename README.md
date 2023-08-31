# NIST-SURF-2023-Quantum-Networks
Code and data for my smmer research. 

Explanation of file names:

Names of the data folders:
- All the parameters of the data collection on the name of the data folder. It should be self-explanatory by the units which number is bin size, number of bins, number of histograms, integration time, etc. When processing data, ensure that these parameters match the corresponding parameters in the code for data processing. 

In the data folders:
- Time corresponds to the real time of each histogram. Time and Data should be of the same length, so each element in Time corresponds to the real time of when the histogram in Data was taken. 
- Data corresponds to the full data. In most cases this is a 2d array, where each element is an array representing a histogram. The bin size and number of bins can be obtained from the folder name. 
- Peaks is a 1d array where each element is the peak of each histogram in Data. 
- Some of the data folders have miscellaneous files. The important files are the ones ending in .npy and .png, as these are the data and figures. Any other file was created for various miscellaneous purposes. 
