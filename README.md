# Crypto Tree Decision Model
The target of this model is to predict which action perform between BUY, SELL and HOLD.

It works with Binance exchange and has been tested on BTC/USDT pair.

## COMPONENTS
First fill settngs tab with your values

### PREPROCESSING
Download candles from binance exchange and adds technical indicators.

### First Part
Compile target variable thanks to scipy and finds local minimum and maximum.
OUTPUT: Action variable -> HOLD or NOT HOLD

### MODEL BUILDER

Build three types of three:
1) Decision tree classifier - gini criterion
2) Decision tree classifier - information gain (entropy criterion)
3) Decision tree regressor - mean squared error (mse) criterion

and output scores for those models

#### Add-on: Feature Selection
Select some indicators and use preprocessing_fs to create a new xlsx with all the indicators selected before.
Then use feature_selection to compute the feature selection and analyze the output.
Then use model builder like explained before with indicators selected from FS.

### Second Part
Optimize target variable found in first part with proprietary algorithm finding best minimum between two maximum and best maximum between two minimum.
OUTPUT: Action variable -> BUY or SELL

### MODEL BUILDER

Build three types of three:
1) Decision tree classifier - gini criterion
2) Decision tree classifier - information gain (entropy criterion)
3) Decision tree regressor - mean squared error (mse) criterion

and output scores for those models
