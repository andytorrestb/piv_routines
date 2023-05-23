import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np

PIV = pd.read_csv('OpenPIV_syn_img_pair-NEW.txt', sep = '\t') 
PIV.columns = ['x', 'y', 'u', 'v', 'flags', 'mask']
print(PIV)
print(PIV['y'].unique())

PIV = PIV[PIV['y'] == 32.0]

print(len(PIV['y'].unique()))
# print(int(PIV.shape[0]/ len(PIV['y'].unique())))
print(PIV)

# for y in PIV['y'].unique():
#     print(y)

#     print(PIV[PIV['y'] == y])

# for index, row in enumerate(PIV.iterrows()):
#     print(index)

# This can be a fat graph, be patient when running. 
# index = PIV.index.to_list()
# fig, ax = plt.subplots(1, 2, figsize = (30, 5))
# sns.stripplot(ax = ax[0], y = PIV['x'], x = index)
# ax[0].set_xticks(np.arange(0, max(index), step=5)) # set x labels.
# ax[0].set_xlabel('index')
# sns.stripplot(ax = ax[1], y = PIV['y'], x = index)
# ax[1].set_xticks(np.arange(0, max(index), step=5))
# plt.show()

ground_truth = pd.read_csv('ground-truth.txt')

# print(ground_truth)
# print(ground_truth['y'].unique())

ground_truth = ground_truth[ground_truth['y'] == 32.0]
print(ground_truth)
# index = ground_truth.index.to_list()
# fig, ax = plt.subplots(1, 2, figsize = (30, 5))
# sns.stripplot(ax = ax[0], y = ground_truth['x'], x = index)
# ax[0].set_xticks(np.arange(0, max(index), step=5)) # set x labels.
# ax[0].set_xlabel('index')
# sns.stripplot(ax = ax[1], y = ground_truth['y'], x = index)
# ax[1].set_xticks(np.arange(0, max(index), step=5))
# plt.show()

