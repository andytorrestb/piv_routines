from matplotlib import pyplot as plt
import seaborn as sns
import inspect
import cv2 as cv
import numpy as np

# Graph histogram of data into a single subplot for visual comparisons.
def histogram_compare(data):
    # Graph all the features of a given data set into a single row.
    # Save to .png files. 
    for dataset in data:
        histogram_features(data[dataset], dataset)

    # Load images into an array.
    img_arr = []
    for index, dataset in enumerate(data):
      img_arr.append(cv.imread(dataset+'.png'))

    # Contatinate graphs into a single image. Save as one file. 
    vis = np.concatenate(tuple(img_arr), axis = 0)
    cv.imwrite('compare.png', vis)

# Graph all the features of a given data set into a single row.
# Helper function for histogram_compare. 
def histogram_features(data, title):
    # Instantanciate the figure object.
    fig, ax = plt.subplots(1, len(data.columns), figsize = (30, 5))

    # Graph histograms of each feature of the dataset 
    # into a single row of graphs. 
    for index, feature in enumerate(data.columns):
        sns.histplot(ax = ax[index], x = data[feature])
        ax[index].set_title(feature)
    
    # Set title and save figure to file. 
    fig.suptitle(title, fontsize = 22, fontweight = 'bold', y = 1.02)
    fig.savefig(title+'.png', dpi = 300, bbox_inches='tight')