from feature_selection_functions import *
import pandas as pd

# df = preprocessing.tabella

df = pd.read_excel('data/01-01-2019_30-05-2019_fs.xlsx', index_col=0)

# univariate selection
uni_sel(df)

# recursive feature
rec_feat(df)

# feature importance
feat_imp(df)

