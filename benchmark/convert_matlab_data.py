import pandas as pd

data = pd.read_csv('exp1_001_b.vec', header = None, delim_whitespace = True)
columns = ['x', 'y', 'u', 'v', 'CHC']
data.columns = columns
data = data.drop('CHC', axis = 1)
data.to_csv('exp1_001_b.txt', sep = '\t')

print(data)