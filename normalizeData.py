import csv
import pandas as pd
import numpy as np

file = open(".\\data.csv")
data = pd.read_csv(file, sep=',', header=None)
data = data.values
numbersOnly = data[1:, 1:].astype(np.float)

# dividing datasets into groups
dataSetA = numbersOnly[:, 0:3]
dataSetD = numbersOnly[:, 9:]

# calculating standard deviatrions for each group
standardDeviationA = np.std(dataSetA, axis=1)
standardDeviationD = np.std(dataSetD, axis=1)

# ignoring/suppressing division be zero warning/exception/error
np.seterr(divide='ignore', invalid='ignore')

# calculating mean for each group
totalDataSet = np.concatenate((dataSetA, dataSetD), axis=1)
totalMean = np.mean(totalDataSet, axis=1)
print(totalMean)

# normalizing standard deviation by totalMean
normalizedA = np.divide(standardDeviationA, totalMean)
normalizedD = np.divide(standardDeviationD, totalMean)

print(normalizedA, normalizedD)

# reached end of file, freeing up memory by removing reference to structures
data = None
numbersOnly = None
dataSetA = None
dataSetD = None
standardDeviationA = None
standardDeviationD = None
meanA = None
meanD = None
