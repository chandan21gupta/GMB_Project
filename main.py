import pandas as pd

class Model:

	def __init__(self,dataset):
		self._dataset = dataset
		self._data = pd.read_csv(self._dataset)

	def checkData(self):
		print(self._data.head())

dataset = input()

model = Model(dataset)

#model.checkData()


