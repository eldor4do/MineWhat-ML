import csv
import nltk
from nltk.corpus import stopwords
import re

def extract_features(featureWords, name, info):
    features = {}
    for word in featureWords:
        features['contains(%s)' % word] = (word in info)
    for token in name.split():
    	features['contains(%s)' % word] = token
    return features

def getFeatureWords():
	with open('products.csv','rb') as f:
		firstLine = False
		mycsv = csv.reader(f)
		listInfoWords = []
		stopW = stopwords.words('english')
		for row in mycsv:
			if firstLine == False: # skipping headers
				firstLine = True
			else:
				info = row[2]
				info = str(info)
				info = info.strip('\'"')

				for w in info.split():
					val = re.search(r"^[a-zA-Z]*$", w) # taking only alphabets, and excluding stop words
					if(w in stopW or val is None):
						continue
					else:
						listInfoWords.append(w)
	
	freqWords = nltk.FreqDist(w.lower() for w in listInfoWords)
	featureWords = list(freqWords)[:1000] # most frequent words
	return featureWords

def train():
	featureWords = getFeatureWords()
	trainingSet = []
	with open('products.csv','rb') as f:
		firstLine = False
		mycsv = csv.reader(f)
		for row in mycsv:
			if firstLine == False:
				firstLine = True
			else:
				cat = row[3]
				name = row[1]
				info = row[2]
				info = str(info)
				info = info.strip('\'"')
				if cat == '["uncategorised"]':
					continue
				else:
					featureVector = extract_features(featureWords,name,info) 
					trainingSet.append((featureVector,cat))
	# Training classifier
	classifier = nltk.NaiveBayesClassifier.train(trainingSet)
	
	# Now to classify
	outCsv = open('products_categorised.csv','wb')
	csvWriter = csv.writer(outCsv)
	with open('products.csv','rb') as f:
		firstLine = False
		mycsv = csv.reader(f)
		for row in mycsv:
			if firstLine == False:
				firstLine = True
				csvWriter.writerow(row)
			else:
				cat = row[3]
				name = row[1]
				info = row[2]
				info = str(info)
				info = info.strip('\'"')
				if cat == '["uncategorised"]':
					category = classifier.classify(extract_features(featureWords, name, info))
					newRow = row
					newRow[3] = category
					csvWriter.writerow(newRow)
				else:
					csvWriter.writerow(row)	
train()