import pandas 
import numpy 
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
from sklearn.ensemble import ExtraTreesClassifier
from utilities import transformer

# 1. Univariate Selection

def uni_sel(df):

	df['MACD_diff'] = transformer(df['MACD_diff'])
	df['CMF'] = transformer(df['CMF'])
	colonne = df.iloc[:, 7:(len(df.columns)-1)]
	print(colonne.columns)
	print('')
	print('Univariate')

	X = df.values[:, 7:(len(df.columns)-1)]
	Y = df.values[:,(len(df.columns)-1)]


	# feature extraction
	test = SelectKBest(score_func=chi2, k=3)
	fit = test.fit(X, Y)

	# summarize scores
	numpy.set_printoptions(precision=3)
	print(fit.scores_)
	features = fit.transform(X)

	# summarize selected features
	print(features[0:5,:])
	print('')
	
# 2. Recursive Feature Elimination

def rec_feat(df):
	print('Recursive Feature Elimination')

	X = df.values[:, 7:(len(df.columns)-1)]
	Y = df.values[:,(len(df.columns)-1)]

	# feature extraction
	model = LogisticRegression()
	rfe = RFE(model, 3)
	fit = rfe.fit(X, Y)
	print("Num Features: ", fit.n_features_)
	print("Selected Features: ", fit.support_)
	print("Feature Ranking: ", fit.ranking_)
	print('')
	
# 3. Feature Importance
	
def feat_imp(df):
	print('Feature Importance')

	X = df.values[:, 7:(len(df.columns)-1)]
	Y = df.values[:,(len(df.columns)-1)]

	# feature extraction
	model = ExtraTreesClassifier()
	model.fit(X, Y)
	print(model.feature_importances_)
	print('')


