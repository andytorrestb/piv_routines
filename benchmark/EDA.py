from matplotlib import pyplot as plt
import seaborn as sns
import inspect
import cv2 as cv
import numpy as np

def compare_summary_stats(data):
  print()
  print('======================================================== Summary Statistics =================================================================')
  for dataset in data:
    if data.columns.contains('flags'):
      data[dataset] = data[dataset].drop(['flags'])
    if data.columns.contains('mask'):
      data[dataset] = data[dataset].drop(['mask'])
    # data[dataset] = data[dataset].drop(['flags', 'mask'], axis = 1)
    print_summary_stats(data[dataset], dataset)
  print('=============================================================================================================================================')
  print()

def print_summary_stats(data, title):
  print(title, end = "|")
  for feature in data:
    p = 3
    mean = round(data[feature].mean(), p)
    if abs(mean) < 10:
      mean = str.format('{0:1.5f}', round(data[feature].mean(), p))
    elif abs(mean) < 100:
      mean = str.format('{0:2.4f}', round(data[feature].mean(), p))
    else:
      mean = str.format('{0:1.1e}', round(data[feature].mean(), p))
    std = round(data[feature].std(), p)
    # std = str.format('{0:.3f}', round(data[feature].std(), p))

    if abs(std) < 10:
      std = str.format('{0:1.5f}', round(data[feature].std(), p))
    elif abs(std) < 100:
      std = str.format('{0:2.4f}', round(data[feature].std(), p))
    else:
      std = str.format('{0:1.1e}', round(data[feature].std(), p))
    print(feature + ':', 'mean =', mean, 'std =', std, end = "|")

  print()

# Assumes that images have been produced and saved in the "results/" folder for each data set.
def find_max_width(data):
  max_width = 0
  for dataset in data:
    # Read in image
    img = cv.imread('results/'+dataset+'.png')
    print(data[dataset].shape)
    print(img.shape)

    if img.shape[1] > max_width:
      max_width = img.shape[1]

  return max_width

# Graph histogram of data into a single subplot for visual comparisons.
def histogram_compare(data):
    # Graph all the features of a given data set into a single row.
    # Save to .png files. 
    for dataset in data:
      histogram_features(data[dataset], dataset)

    max_width = find_max_width(data)

    # Load images into an array.
    img_arr = []
    for index, dataset in enumerate(data):
        image = cv.imread('results/' + dataset + '.png')
        # Resize the image to a common width
        image = cv.resize(image, (max_width, image.shape[0]))
        img_arr.append(image)

    # Contatinate graphs into a single image. Save as one file.
    vis = np.concatenate(tuple(img_arr), axis = 0)
    cv.imwrite('results/compare.png', vis)

# Graph all the features of a given data set into a single row.
# Helper function for histogram_compare. 
def histogram_features(data, title):
    print(title)
    # input()
    # Instantanciate the figure object.
    fig, ax = plt.subplots(1, len(data.columns), figsize = (30, 5))

    # Graph histograms of each feature of the dataset 
    # into a single row of graphs. 
    for index, feature in enumerate(data.columns):
        sns.histplot(ax = ax[index], x = data[feature])
        ax[index].set_title(feature)
    
    # Set title and save figure to file. 
    fig.suptitle(title, fontsize = 22, fontweight = 'bold', y = 1.02)
    fig.savefig('results/'+title+'.png', dpi = 300, bbox_inches='tight')

# Execute direct comparison of data by plotting each feature.
def plot_features(data):
  # Set font dictionary
  font_axis_publish = {
        'color':  'black',
        'weight': 'bold',
        'size': 22,
        }

  # Save the names of the different data sets  (results) to be compared.
  keys = list(data.keys())

  # Save the names of the features for the data sets to be compared.
  # To do: Compare these features to make sure they are the same, clean if needed.
  features = data[keys[0]].columns

  # Instantanciate the figure object.
  fig, ax = plt.subplots(1, len(features), figsize = (30, 5))

  for index, feature in enumerate(features):
    # Save number of data points for each feature
    index_values = np.array(data[keys[0]][feature].index)

    # Graph the data in each feature
    # To Do: Move this to a for loop iterating over "keys"
    ax[index].plot(index_values, data[keys[0]][feature].values, label = keys[0])
    ax[index].plot(index_values, data[keys[1]][feature].values, label = keys[1])

    # Set informational text data.
    ax[index].set_title(feature,  fontdict = font_axis_publish)
    ax[index].legend()

    # Printing data type to help debug (if needed)
    # print(type(data[keys[0]][feature].index))
    # print(index, feature)
    # print(keys[0], keys[1])

  fig.savefig('results/feature_comp.png', dpi = 300, bbox_inches='tight')