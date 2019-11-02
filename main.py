import pandas as pd
import seaborn as sns
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

	# def addIQR(self):
	# 	self._data['A_IQR'] = self._data[['A_1','A_2','A_3','A_4']].std(axis=1)
	# 	self._data['B_IQR'] = self._data[['B_1','B_2','B_3','B_4']].std(axis=1)
	# 	self._data['C_IQR'] = self._data[['C_1','C_2','C_3','C_4']].std(axis=1)	
	# 	self._data['D_IQR'] = self._data[['D_1','D_2','D_3','D_4']].std(axis=1)

	def addZscore(self):
		self._data['A_Z'] = (self._data['A_mean'] - self._data['A_mean'].mean())/self._data['A_SD'].std()
		self._data['B_Z'] = (self._data['B_mean'] - self._data['B_mean'].mean())/self._data['B_SD'].std()
		self._data['C_Z'] = (self._data['C_mean'] - self._data['C_mean'].mean())/self._data['C_SD'].std()
		self._data['D_Z'] = (self._data['D_mean'] - self._data['D_mean'].mean())/self._data['D_SD'].std()

	def normalize(self):
		self._data['A_normalize'] = self._data['A_SD']/self._data['A_mean']
		self._data['B_normalize'] = self._data['B_SD']/self._data['B_mean']
		self._data['C_normalize'] = self._data['C_SD']/self._data['C_mean']
		self._data['D_normalize'] = self._data['D_SD']/self._data['D_mean']

	def order(self):
		a_var = self._data['A_normalize'].mean()
		b_var = self._data['B_normalize'].mean()
		c_var = self._data['C_normalize'].mean()
		d_var = self._data['D_normalize'].mean()

		list = [a_var,b_var,c_var,d_var]
		list.sort()
		position = []
		for i in list:
			if(i == a_var):
				position.append("A")
			elif(i == b_var):
				position.append("B")
			elif(i == c_var):
				position.append("C")
			else:
				position.append("D")
		print(position)q

	def outlier_Z(self,col):
		if(col['A_Z'] < 3 and col['A_Z'] > -3):
			if((col['B_Z'] < 3 and col['B_Z'] > -3) and (col['C_Z'] < 3 and col['C_Z'] > -3)):
				return "Yes"
			elif((col['C_Z'] < 3 and col['C_Z'] > -3) and (col['D_Z'] < 3 and col['D_Z'] > -3)):
				return "Yes"
			elif((col['D_Z'] < 3 and col['D_Z'] > -3) and col['B_Z'] < 3 and col['B_Z']):
				return "Yes"
			return "No"

		elif(col['B_Z'] < 3 and col['B_Z'] > -3):
			if((col['C_Z'] < 3 and col['C_Z'] > -3) and (col['D_Z'] < 3 and col['D_Z'] > -3)):
				return "Yes"
			return "No"
		return "No"


	def add_outlier_Z(self):
		self._data['outlier_Z'] = self._data.apply(self.outlier_Z,axis = 1)

dataset = "Simulated_data_ageing.csv"
model = Model(dataset)

model.addMean()
model.addSD()
model.normalize()

#model.checkData()

model.addZscore()

#model.order()

model.add_outlier_Z()

model.checkData()






