import pandas as pd
from scipy.stats import ttest_ind
import numpy as np
import matplotlib.cm as cm
import math
import matplotlib.pyplot as plt

#import seaborn as sns
class Model:

	def __init__(self,dataset):
		self._dataset = dataset
		self._data = pd.read_csv(self._dataset)

	def checkData(self):
		print(self._data.head())

	def addMean(self):
		self._data['mean_per_gene'] = self._data[['A_1','A_2','A_3','B_1','B_2','B_3','C_1','C_2','C_3','D_1','D_2','D_3']].mean(axis=1)

	def addSD(self):
		self._data['A_SD'] = self._data[['A_1','A_2','A_3']].std(axis=1)
		self._data['B_SD'] = self._data[['B_1','B_2','B_3']].std(axis=1)
		self._data['C_SD'] = self._data[['C_1','C_2','C_3']].std(axis=1)
		self._data['D_SD'] = self._data[['D_1','D_2','D_3']].std(axis=1)

	# def addIQR(self):
	# 	self._data['A_IQR'] = self._data[['A_1','A_2','A_3','A_4']].std(axis=1)
	# 	self._data['B_IQR'] = self._data[['B_1','B_2','B_3','B_4']].std(axis=1)
	# 	self._data['C_IQR'] = self._data[['C_1','C_2','C_3','C_4']].std(axis=1)	
	# 	self._data['D_IQR'] = self._data[['D_1','D_2','D_3','D_4']].std(axis=1)

	def addZscore(self):
		self._data['A_Z'] = (self._data['A_normalize'] - self._data['A_normalize'].mean())/self._data['A_normalize'].std()
		self._data['B_Z'] = (self._data['B_normalize'] - self._data['B_normalize'].mean())/self._data['B_normalize'].std()
		self._data['C_Z'] = (self._data['C_normalize'] - self._data['C_normalize'].mean())/self._data['C_normalize'].std()
		self._data['D_Z'] = (self._data['D_normalize'] - self._data['D_normalize'].mean())/self._data['D_normalize'].std()

	def normalize(self):
		self._data['A_normalize'] = self._data['A_SD']/self._data['mean_per_gene']
		self._data['B_normalize'] = self._data['B_SD']/self._data['mean_per_gene']
		self._data['C_normalize'] = self._data['C_SD']/self._data['mean_per_gene']
		self._data['D_normalize'] = self._data['D_SD']/self._data['mean_per_gene']

	def mean_t_test_p_value(self):
		self._data['A_MEAN'] = self._data[['A_1','A_2','A_3']].mean(axis=1)
		self._data['D_MEAN'] = self._data[['D_1','D_2','D_3']].mean(axis=1)
		self._data['FC'] = np.log2(self._data['D_MEAN']/self._data['A_MEAN'])
		self._data['t_test']=ttest_ind(self._data.loc[:,['A_1','A_2','A_3']],self._data.loc[:,['D_1','D_2','D_3']], axis=1)[0]
		self._data['p_value']=np.log10(ttest_ind(self._data.loc[:,['A_1','A_2','A_3']],self._data.loc[:,['D_1','D_2','D_3']], axis=1)[1])
		self._data['p_value']=-self._data['p_value']

	def volcano_plot(self):
		labels = self._data['gene_short_name']
		x = self._data['FC']
		y = self._data['p_value']
		clrs = []
		genes_in_threshold=[]
		count=0
		for i in range(0, len(x)):
			if x[i]>2 or x[i]<-2:
				if y[i] > 1.3:
					count+=1
					genes_in_threshold.append(labels[i])
					clrs.append(1)
				else:
					clrs.append(0)
			else:
				clrs.append(0)
		area = np.pi*1
		print(genes_in_threshold)
		fig, ax = plt.subplots(figsize=(20, 20))
		colors = ['#2300A8', '#00A658']
		ax.scatter(x, y, alpha=0.70, c=clrs, cmap=cm.brg)
		ax.set_title('GMB 0.3')
		ax.set_xlabel('log2(Fold Change)')
		ax.set_ylabel('log10(1/p_value)')
		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.grid(color='grey', linestyle='-', linewidth=0.25, alpha=0.5)
		plt.show()

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
		print(position)

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

	def add_IQR(self):
		Q1 = self._data.loc[:,['A_normalize', 'B_normalize', 'C_normalize', 'D_normalize']].quantile(0.25)
		Q3 = self._data.loc[:,['A_normalize', 'B_normalize', 'C_normalize', 'D_normalize']].quantile(0.75)
		IQR = Q3-Q1
		normalizedCols = self._data.loc[:,['A_normalize', 'B_normalize', 'C_normalize', 'D_normalize']]
		checkOutliers = ((normalizedCols < (Q1 - 1.5 * IQR)) | (normalizedCols > (Q3 + 1.5 * IQR))).any(axis=1)
		self._data['outlier_IQR'] = checkOutliers

	def mean(self):
		self._data['A_mean'] = self._data[['A_1','A_2','A_3']].mean(axis=1)
		self._data['D_mean'] = self._data[['D_1','D_2','D_3']].mean(axis=1)

	def variance(self):
		self._data['A_variance'] = self._data[['A_1','A_2','A_3']].var(axis=1)
		self._data['D_variance'] = self._data[['D_1','D_2','D_3']].var(axis=1)

	def t_test(self):
		self._data['T_mean'] = abs(self._data['A_mean']-self._data['D_mean'])/(((self._data['A_variance']))+(self._data['D_variance'])/3)**(0.5)
		#self._data.sort_values(by="T_mean")

dataset = "Simulated_data_ageing.csv"
model = Model(dataset)

model.addMean()
model.addSD()
model.normalize()


model.mean()
model.variance()
#model.t_test()
model.mean_t_test_p_value()
#model.checkData()
model.volcano_plot()

#model.checkData()

#model.addZscore()

#model.order()

#model.add_outlier_Z()

#model.variance()

#model.sample()

#model.checkData()





