# -*- coding: utf-8 -*-
"""Untitled21.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1fyJ7BAZjvQzbjDU3jWBdGZJOCyczhxtC
"""

#Final code with steps
# Step 1 - Import the library and load data
# Load CSV Using Python Standard Library
import csv
import numpy
import matplotlib.pyplot as plt
filename = 'train_imperson_without4n7_balanced_data.csv'
raw_data = open(filename, 'rt')
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
x = list(reader)
data = numpy.array(x).astype('float')
print(data.shape)
print('\n')

#Load CSV Using Python Standard Library
import csv
import numpy
filename = 'test_imperson_without4n7_balanced_data.csv'
raw_data = open(filename, 'rt')
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
x = list(reader)
data = numpy.array(x).astype('float')
print(data.shape)
print('\n')
#VarianceThreshold was performed for Data analysis 
from sklearn.feature_selection import VarianceThreshold
import csv
import pandas as pd
threshold_n=0.95
filename = 'train_imperson_without4n7_balanced_data.csv'
raw_data = open(filename, 'rt')
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
#x = list(reader)
x = pd.DataFrame(reader)
sel = VarianceThreshold(threshold=(threshold_n*(1 - threshold_n)))
sel_var = sel.fit_transform(x)
print(x[sel.get_support(indices=True)])

import pandas as pd
import csv
import numpy as np
from sklearn.feature_selection import VarianceThreshold

#Step 2 - Setup the Data
threshold_n = 0.95
filename = 'train_imperson_without4n7_balanced_data.csv'
raw_data = open(filename, 'rt')
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
x = pd.DataFrame(reader)
x = x[1:]
x_features, x_label = x.iloc[:, : -1], x.iloc[:, [-1]]
sel = VarianceThreshold(threshold=(threshold_n*(1 - threshold_n)))
sel_var = sel.fit_transform(x_features)
x_features[sel.get_support(indices=True)]
y = x_features[sel.get_support(indices=True)]
print(y)
y = y.astype(float)
#Creating the Correlation matrix and Selecting the Upper trigular matrix
#to drop out highly correlated features using Python from the data set
#but as we are using selectkbest for feature selection it will as it is select the best
cor_matrix = y.corr().abs()
print(cor_matrix)
print('\n')
#box, whisker, density plots
#1 Univariate Histograms
from matplotlib import pyplot
y.hist()
plt.figure(figsize=(20,10))
pyplot.show()
print('\n')
print('\n')
#2 Density Plots
y.plot(kind='density', subplots=True, layout=(10,2), sharex=False)
plt.figure(figsize=[200,100])
fig=pyplot.figure()
fig.tight_layout()
pyplot.show()
print('\n')
print('\n')
#step 3 Feature Extraction using PCA
# feature extraction
from sklearn.decomposition import PCA
#I have to separate the target variable from the data, then I do pca on the feature variables
#and then select the top principal componenent and add this to the feature variable
#then do selectkbest on this combined dataset. The combined datasets you use to test
#what the best algorithm is.
# feature extraction to select the top 10 principal components
pca = PCA(n_components=10)
pca.fit(x_features)
fe = pca.transform(x_features)
print(fe)
#to combine fe with the original data without the target variable that is x_features
combineddataset = np.hstack((x_features, fe))
print(combineddataset.shape)
print('\n')

#Step 4 Feature Scaling using MinMaxScalar on the combineddataset obtained from pca
from sklearn.preprocessing import MinMaxScaler
from numpy import set_printoptions
#resacle data between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))
rescaledX = scaler.fit_transform(combineddataset)
# summarize transformed data
set_printoptions(precision=3)
print(rescaledX)
print('\n')

#step 5 Feature Selection using selectkbest
print('selectKbest')
from numpy import set_printoptions
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
print(rescaledX)
rescaledX=pd.DataFrame(rescaledX)
test = SelectKBest(score_func=chi2, k=10)
fs = test.fit(rescaledX, x_label)
# summarize scores
set_printoptions(precision=3)
#print(fit.score_)
features = fs.transform(rescaledX)
# summarize selected features
print(features)
print(features.shape)
print('\n')

#step6 for selectkbest data
#checking which algorithm to use for the pca data
# Compare Algorithms
from matplotlib import pyplot
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
# prepare models
models = []
models.append(('LR', LogisticRegression(solver='liblinear')))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('NB', GaussianNB()))
models.append(('SVM', SVC()))
# evaluate each model in turn
results = []
names = []
scoring = 'accuracy'
for name, model in models:
  kfold = KFold(n_splits=10, random_state=7,shuffle=True)
  cv_results = cross_val_score(model, features, x_label, cv=kfold, scoring=scoring)
  results.append(cv_results)
  names.append(name)
  msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
  print(msg)
# boxplot algorithm comparison
fig = pyplot.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
pyplot.boxplot(results)
ax.set_xticklabels(names)
pyplot.show()
print('\n')
print('\n')
#so the data from the selectkbest using KNN algorithm shows the best accuracy of 0.997733 as compared to CART: 0.997022
#but I chose CART as decision trees are interpretable

#step 7refining algorithms
#using grid search to decide the best hyperpermeter
from sklearn import tree
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
#we are using Decision Tree Classifier as 
#a Machine Learning model to use GridSearchCV. So we have created an object dec_tree.
dec_tree = tree.DecisionTreeClassifier()
#Using Pipeline for GridSearchCV
pipe = Pipeline(steps=[('dec_tree', dec_tree)])
#GridSearchCV will select the best value of parameter.
criterion = ['gini', 'entropy']
max_depth = [2,4,6,8,10,12]
#Now we are creating a dictionary to set all the parameters 
#options for different objects.
parameters = dict(dec_tree__criterion=criterion,
                      dec_tree__max_depth=max_depth)
#Making an object clf_GS for GridSearchCV and fitting the dataset i.e X and y
clf_GS = GridSearchCV(pipe, parameters)
clf_GS.fit(features, x_label)
#Now we are using print statements to print the results. 
#It will give the values of hyperparameters as a result.
print('Best Criterion:', clf_GS.best_estimator_.get_params()['dec_tree__criterion'])
print('Best max_depth:', clf_GS.best_estimator_.get_params()['dec_tree__max_depth'])
print(); print(clf_GS.best_estimator_.get_params()['dec_tree'])
#the best parameter were the criteria = entropy and max_depth=4
print('\n')


#step 8
#best configuration model
clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=4)
clf.fit(features, x_label)
plt.figure(figsize=(20,10))
tree.plot_tree(clf, filled=True, fontsize=14)
plt.show()
print('\n')


#step9
#Once i got the best classifier that is CART, and the best hyperperameters then testing it on test dataset
#it will test the true performance of the model
#Load CSV Using Python Standard Library
#step a import the test data
import csv
import numpy
import pandas as pd
from sklearn.feature_selection import VarianceThreshold
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler
from numpy import set_printoptions
from numpy import set_printoptions
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

filename = 'test_imperson_without4n7_balanced_data.csv'
raw_data = open(filename, 'rt')
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
y = list(reader)
data = numpy.array(x).astype('float')
print(data.shape)
print('\n')
#step b separate the target variable
#VarianceThreshold was performed for Data analysis 
threshold_n=0.95
filename = 'test_imperson_without4n7_balanced_data.csv'
raw_data = open(filename, 'rt')
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
#x = list(reader)
x = pd.DataFrame(reader)
sel = VarianceThreshold(threshold=(threshold_n*(1 - threshold_n)))
sel_var = sel.fit_transform(x)
print(x[sel.get_support(indices=True)])
print('\n')
# to remove the first row and separate the target variable
#Step 2 - Setup the Data
threshold_n = 0.95
filename = 'test_imperson_without4n7_balanced_data.csv'
raw_data = open(filename, 'rt')
reader = csv.reader(raw_data, delimiter=',', quoting=csv.QUOTE_NONE)
x = pd.DataFrame(reader)
x = x[1:]
x_features, x_label = x.iloc[:, : -1], x.iloc[:, [-1]]
sel = VarianceThreshold(threshold=(threshold_n*(1 - threshold_n)))
sel_var = sel.fit_transform(x_features)
x_features[sel.get_support(indices=True)]
y = x_features[sel.get_support(indices=True)]
print(y)
y = y.astype(float)
print('\n')
#have a question about applying pca on 152 insted of 151
#step 3 Feature Extraction using PCA
#I have to separate the target variable from the data, then I do pca on the feature variables
#and then select the top principal componenent and add this to the feature variable
#then do selectkbest on this combined dataset. The combined datasets you use to test
# feature extraction to select the top 10 principal components


fe_test = pca.transform(x_features)
print(fe_test)

#to combine fe with the original data without the target variable that is x_features
combineddataset_test = np.hstack((x_features, fe_test))
print(combineddataset_test.shape)
print('\n')
#there some negative numbers so I performed scaling on combineddataset
#resacle data between 0 and 1
scaler = MinMaxScaler(feature_range=(0, 1))
rescaledX_test = scaler.fit_transform(combineddataset_test)
# summarize transformed data
set_printoptions(precision=3)
print(rescaledX_test)
print('\n')
print('here I used .get_support()param of feature_selection to get the feature names from the initial dataset')
rescaledX_test=pd.DataFrame(rescaledX_test)
fe_column_names = list(rescaledX_test.columns[test.get_support()])
best_columns = rescaledX_test[fe_column_names]
print(best_columns.shape)
print('\n')
y_pred = clf.predict(best_columns)
#y_pred is the predicted label

from sklearn.metrics import classification_report, confusion_matrix
#the confusion matrix is performed on the predicted label and the true label
print(confusion_matrix(y_pred, x_label))
print(classification_report(y_pred, x_label))
#From the confusion matrix you can see that out of 40158 test instances
#the algorithm misclassified only 15530. This gives a 61.3 % accuracy