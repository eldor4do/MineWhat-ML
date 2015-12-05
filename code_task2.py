import csv
import numpy as np 
from sklearn.preprocessing import Imputer
from sklearn import linear_model
import pandas as pd

def train():

	with open('products.csv','rb') as f:
			firstLine = False
			mycsv = csv.reader(f)
			ls = []
			ls1 = []
			ls2 = []
			ls4_1 = []
			ls4_2 = []
			for row in mycsv:
				if firstLine == False:
					firstLine = True
				else:
					p1 = row[5]
					p2 = row[6]
					p4 = row[8]
					if len(p1) == 0:
						continue
					else:
						p1=int(p1)
						p4_1=int(p4)
						ls1.append(p1)
						ls4_1.append(p4_1)
					if len(p2) == 0:
						continue
					else:
						p2=int(p2)
						p4_2=int(p4)
						ls2.append(p2)
						ls4_2.append(p4_2)
						
			d1 = pd.DataFrame(ls1)
			d4_1 = pd.DataFrame(ls4_1)
			d2 = pd.DataFrame(ls2)
			d4_2 = pd.DataFrame(ls4_2)
			regr1 = linear_model.LinearRegression()
	 		regr1.fit(d4_1, d2)
	 		regr2 = linear_model.LinearRegression()
	 		regr2.fit(d4_2, d2)
 		
 	return regr1, regr2
def predict():
	regr1, regr2 = train()
	with open('products.csv','rb') as f:
		firstLine = False
		mycsv = csv.reader(f)
		outCsv = open('products_predicted.csv','wb')
		csvWriter = csv.writer(outCsv)
		for row in mycsv:
				if firstLine == False:
					firstLine = True
					newRow = row
					csvWriter.writerow(newRow)
				else:
					newRow = row
					p1 = row[5]
					p2 = row[6]
					p4 = int(row[8])
					if len(p1) == 0:
						predictedValue = regr1.predict(p4)
						newRow[5] = int(predictedValue)
					if len(p2) == 0:
						predictedValue = regr2.predict(p4)
						newRow[6] = int(predictedValue)
					csvWriter.writerow(newRow)

predict()