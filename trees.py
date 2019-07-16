import numpy as np
import pandas as pd
import sklearn
from sklearn import tree
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import export_graphviz
from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.tree import DecisionTreeRegressor  
from sklearn import svm
import collections
import pydotplus
import pickle
from utilities import tree_model_name
import settings

def Gini(df):	
	df = df.dropna()
	X = df.values[:, 7:(len(df.columns)-1)]
	Y = df.values[:,(len(df.columns)-1)]

	# split in train e test
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 100)

	clf_gini = DecisionTreeClassifier(criterion = "gini", random_state = 100,
								   max_depth=15, min_samples_leaf=5)

	clf_gini.fit(X_train, y_train)

	DecisionTreeClassifier(class_weight=None, criterion='gini', max_depth=15,
				max_features=None, max_leaf_nodes=None, min_samples_leaf=5,
				min_samples_split=2, min_weight_fraction_leaf=0.0,
				presort=False, random_state=100, splitter='best')

	y_pred = clf_gini.predict(X_test)
	
	print('Saving model')
	model_name = 'Gini'
	model_name = tree_model_name(model_name)

	# Open the file to save as pkl file
	feature = df.iloc[:,7:(len(df.columns)-1)]
	data_feature_names = list(feature.columns.values)

	decision_tree_model_pkl = open(model_name, 'wb')
	pickle.dump(clf_gini, decision_tree_model_pkl)

	dot_data = tree.export_graphviz(clf_gini,
									feature_names=data_feature_names,
									out_file=None,
									filled=True,
									rounded=True)
	graph = pydotplus.graph_from_dot_data(dot_data)

	colors = ('turquoise', 'orange')
	edges = collections.defaultdict(list)

	for edge in graph.get_edge_list():
		edges[edge.get_source()].append(int(edge.get_destination()))

	for edge in edges:
		edges[edge].sort()    
		for i in range(2):
			dest = graph.get_node(str(edges[edge][i]))[0]
			dest.set_fillcolor(colors[i])
			
	return [X_train, X_test, y_train, y_test, y_pred,  graph];
	
def Entropy(df):	
	df = df.dropna()
	X = df.values[:, 7:(len(df.columns)-1)]
	Y = df.values[:,(len(df.columns)-1)]

	# split in train e test
	X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = 0.3, random_state = 100)

	clf_entropy = DecisionTreeClassifier(criterion = "entropy", random_state = 100,
                               max_depth=5, min_samples_leaf=2)
	clf_entropy.fit(X_train, y_train)

	DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=5,
            max_features=None, max_leaf_nodes=None, min_samples_leaf=2,
            min_samples_split=2, min_weight_fraction_leaf=0.0,
            presort=False, random_state=100, splitter='best')

	y_pred = clf_entropy.predict(X_test)
	
	print('Saving model')
	model_name = 'Entropy'
	model_name = tree_model_name(model_name)

	# Open the file to save as pkl file
	feature = df.iloc[:,7:(len(df.columns)-1)]
	data_feature_names = list(feature.columns.values)

	decision_tree_model_pkl = open(model_name, 'wb')
	pickle.dump(clf_entropy, decision_tree_model_pkl)

	dot_data = tree.export_graphviz(clf_entropy,
									feature_names=data_feature_names,
									out_file=None,
									filled=True,
									rounded=True)
	graph = pydotplus.graph_from_dot_data(dot_data)

	colors = ('turquoise', 'orange')
	edges = collections.defaultdict(list)

	for edge in graph.get_edge_list():
		edges[edge.get_source()].append(int(edge.get_destination()))

	for edge in edges:
		edges[edge].sort()    
		for i in range(2):
			dest = graph.get_node(str(edges[edge][i]))[0]
			dest.set_fillcolor(colors[i])
			
	return [X_train, X_test, y_train, y_test, y_pred, graph];

# REGRESSOR TREE

def Regr(df):
	lb_make = LabelEncoder()
	df['Action'] = lb_make.fit_transform(df['Action'])
	binary = df['Action'].copy()
	# for i in range(len(df)):
	# 	if binary[i] == 'Hold':
	# 		binary[i] = 0
	# 		binary[i] == int(binary[i])
	# 	elif binary[i] == 'No_Hold':
	# 		binary[i] = 1
	# 		binary[i] == int(binary[i])
	#df['Action'] = binary
	df = df.dropna()
	X = df.values[:, 7:(len(df.columns)-1)]
	Y = df.values[:,(len(df.columns)-1)]

	# split in train e test
	X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)

	regressor = DecisionTreeRegressor(random_state = 0) 	
	regressor.fit(X_train, y_train)

	DecisionTreeRegressor(criterion='mse', max_depth=None,
					max_features=None, max_leaf_nodes=None, min_samples_leaf=1,
					min_samples_split=2, min_weight_fraction_leaf=0.0,
					presort=False, random_state=100, splitter='best')	
	y_pred = regressor.predict(X_test)
	return [X_train, X_test, y_train, y_test, y_pred, regressor];
