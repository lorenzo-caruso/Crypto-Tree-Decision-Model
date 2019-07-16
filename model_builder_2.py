from trees import *
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

# df = preprocessing.tabella

df2 = pd.read_excel('data/01-01-2019_30-05-2019_albero2.xlsx', index_col=0)

df = df2.loc[df2['Action'] != 'Hold']

df.reset_index(drop=True, inplace=True)

gini = Gini(df)

X_train = gini[0]
X_test = gini[1]
y_train = gini[2]
y_test = gini[3] 
y_pred = gini[4]
graph = gini[5]

print("Gini")
print("Accuracy is ", accuracy_score(y_test,y_pred)*100)
print(classification_report(y_test, y_pred)) 

graph.write_png('tree/Gini_tree.png')

############################################
entropy = Entropy(df)

X_train = entropy[0]
X_test = entropy[1]
y_train = entropy[2]
y_test = entropy[3] 
y_pred = entropy[4]
graph = entropy[5]

print("Entropy")
print("Accuracy is ", accuracy_score(y_test,y_pred)*100)
print(classification_report(y_test, y_pred)) 

graph.write_png('tree/Entropy_tree_2.png')

############################################

regressor = Regr(df)

X_train = regressor[0]
X_test = regressor[1]
y_train = regressor[2]
y_test = regressor[3] 
y_pred = regressor[4]
model = regressor[5]

print("MSE")
model_score = model.score(X_train,y_train)
# Have a look at R sq to give an idea of the fit ,
# Explained variance score: 1 is perfect prediction
print('coefficient of determination R^2 of the prediction: ', model_score)
y_pred = model.predict(X_test)

# The mean squared error
print("Mean squared error: %.2f"% mean_squared_error(y_test, y_pred))
# Explained variance score: 1 is perfect prediction
print('Test Variance score: %.2f' % r2_score(y_test, y_pred))
