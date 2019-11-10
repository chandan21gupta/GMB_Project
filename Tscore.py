import pandas as pd
import numpy as np

file = open(".\\data.csv")
data = pd.read_csv(file)
data = data.values

column1 = np.array(data[1:, 1]).astype(np.float)  # Just an example Column
column2 = np.array(data[1:, 2]).astype(np.float)  # Must be our normalized value

# print(column1, column2)

def calculateT(D, sqD, n):
    numerator = D / n
    denominatorsNumerator = (sqD - ((D ** 2) / n))
    denominatorsdenominator = (n - 1) * n
    finalDenominator = (denominatorsNumerator / denominatorsdenominator) ** 0.5
    t = numerator / finalDenominator
    return t


def getTScore(column1: np.array, column2: np.array):
    column2SubtractedFromColumn1 = np.subtract(column1, column2)
    sumOfDifference = np.sum(column2SubtractedFromColumn1)
    squareOfColumn2SubtractedFromColumn1 = np.power(column2SubtractedFromColumn1, 2)
    sumOfSquareOfDifference = np.sum(squareOfColumn2SubtractedFromColumn1)
    t = calculateT(sumOfDifference, sumOfSquareOfDifference, len(column1))
    return t


t = getTScore(column1, column2)
print(t)