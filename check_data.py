import pandas as pd

df = pd.read_csv('data/raw/WA_Fn-UseC_-Telco-Customer-Churn.csv', nrows=5)
print('Shape:', df.shape)
print('\nColumns:')
print(df.columns.tolist())
print('\nFirst few rows:')
print(df.head())
