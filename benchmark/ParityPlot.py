import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

# def mag(data):
#   mag = np.sqrt(
#       np.square(data['u']) + np.square(data['v']))
  
#   for point in data.iterrows():
#     # print(point)
#     # print(data[point]['u'], point['v'], mag)
#   return mag

def parityPlot(data1, data2):
  # print(data1.shape, data2.shape)
  # Font for figure for publishing
  font_axis_publish = {
        'color':  'black',
        'weight': 'bold',
        'size': 22,
        }
  stats = {}
  for feature in data1.columns:
    # print(feature)
#   y = mag(data1)
#   x = mag(data2)

    y = data1[feature]
    x = data2[feature]

  #   y = data1['x'] / data1['x'].abs().max()
  #   x = data2['x'] / data2['x'].abs().max()

    if len(x) > len(y):
      remove_n = len(x) - len(y)
      drop_indices = np.random.choice(x.index, remove_n, replace=False)
      x = x.drop(drop_indices)
    elif len(x) < len(y):
      remove_n = len(y) - len(x)
      drop_indices = np.random.choice(y.index, remove_n, replace=False)
      y = y.drop(drop_indices)

    fignow = plt.figure(figsize=(8,8))


    bounds = (min(x.min(), y.min()) - int(0.1 * y.min()), max(x.max(), y.max())+ int(0.1 * y.max()))
    # print('bounds:', bounds)

    # Reset the limits
    ax = plt.gca()
    ax.set_xlim(bounds)
    ax.set_ylim(bounds)
    # Ensure the aspect ratio is square
    ax.set_aspect("equal", adjustable="box")

    plt.plot(x,y,"o", alpha=0.5 ,ms=10, markeredgewidth=0.0)

    ax.plot([0, 1], [0, 1], "r-",lw=2 ,transform=ax.transAxes)

    # Calculate Statistics of the Parity Plot
    mean_abs_err = np.mean(np.abs(x-y))
    rmse = np.sqrt(np.mean((x-y)**2))
    rmse_std = rmse / np.std(y)
    # z = np.polyfit(x,y, 1)
    # y_hat = np.poly1d(z)(x)

    p = 3
    # stats[feature] = [round(mean_abs_err, p), round(rmse, p), round(r2_score(y,x), p)]

    # text = f"$\: \: Mean \: Absolute \: Error \: (MAE) = {mean_abs_err:0.3f}$ \n $ Root \: Mean \: Square \: Error \: (RMSE) = {rmse:0.3f}$ \n $ RMSE \: / \: Std(y) = {rmse_std :0.3f}$ \n $R^2 = {r2_score(y,x):0.3f}$"



    # plt.gca().text(0.05, 0.95, text,transform=plt.gca().transAxes,
    #     fontsize=14, verticalalignment='top')

    # Title and labels
    plt.title("Parity Plot " + feature, fontdict=font_axis_publish)
    plt.xlabel('PIV Analysis', fontdict=font_axis_publish)
    plt.ylabel('Ground Truth', fontdict=font_axis_publish)

    # Save the figure into 300 dpi
    fignow.savefig("results/parityplot_"+ feature +"_vals.png",format = "png",dpi=300,bbox_inches='tight')

  return stats