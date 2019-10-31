import pandas as pd

class Model:

	def __init__(self,dataset):
		self._dataset = dataset
		self._data = pd.read_csv(self._dataset)

	def checkData(self):
		print(self._data.head())

	def addMean(self):
		self._data['A_mean'] = self._data[['A_1','A_2','A_3','A_3']].mean(axis=1)
		self._data['B_mean'] = self._data[['B_1','B_2','B_3','B_3']].mean(axis=1)
		self._data['C_mean'] = self._data[['C_1','C_2','C_3','C_3']].mean(axis=1)
		self._data['D_mean'] = self._data[['D_1','D_2','D_3','D_3']].mean(axis=1)

	def addSD(self):
		self._data['A_SD'] = self._data[['A_1','A_2','A_3','A_3']].std(axis=1)
		self._data['B_SD'] = self._data[['B_1','B_2','B_3','B_3']].std(axis=1)
		self._data['C_SD'] = self._data[['C_1','C_2','C_3','C_3']].std(axis=1)
		self._data['D_SD'] = self._data[['D_1','D_2','D_3','D_3']].std(axis=1)

	def addVariation(self):
		self._data['A_variation'] = self._data['A_SD']/self._data['A_mean']
		self._data['B_variation'] = self._data['B_SD']/self._data['B_mean']
		self._data['C_variation'] = self._data['C_SD']/self._data['C_mean']
		self._data['D_variation'] = self._data['D_SD']/self._data['D_mean']

dataset = "Simulated_data_ageing.csv"
model = Model(dataset)

model.addMean()
model.addSD()
model.addVariation()

model.checkData()


