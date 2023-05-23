import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt

sig2noise = np.linspace(1.05, 2, 51)
# kernal_size = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1]
kernel_size = range(1, 21)

# Make files to hold stat data. 
data = open('benchmarking_stats.csv', 'w')
# data.write('s2n,x_abs,x_rmse,x_r2,y_abs,y_rmse,y_r2,u_abs,u_rmse,u_r2,v_abs,v_rmse,v_r2\n')

# for s2n in sig2noise:
#     print(round(s2n, 3))

#     str_s2n = str(round(s2n, 3))

#     # Make directory to hold results. 
#     cwd = os.getcwd() + '/' + str_s2n
#     if not os.path.isdir(cwd):
#         os.makedirs(cwd)

#     # Run PIV analysis using current sig2noise value. 
#     os.system('python3 automated_study_sweep.py ' + str_s2n)

for kernel in kernel_size:
    str_kernel = str(kernel)
    cwd = os.getcwd() + '/' + str_kernel
    if not os.path.isdir(cwd):
        os.makedirs(cwd)

    os.system('python3 automated_study_sweep.py ' + str_kernel)


# Read benchmarking statistics from saved file. 
benchmarking_stats = pd.read_csv('benchmarking_stats.csv', header = None)
benchmarking_stats.columns = [
    's2n',
    'x_abs','x_rmse','x_r2',
    'y_abs','y_rmse','y_r2',
    'u_abs','u_rmse','u_r2',
    'v_abs','v_rmse','v_r2'
]

print(benchmarking_stats)

# Plot benchmarking statistics
font_axis_publish = {
        'color':  'black',
        'weight': 'bold',
        'size': 22,
        }

x_label = 'Kernel Size'

plt.subplot(1, 2, 1)
plt.title('R^2 score for U', fontdict = font_axis_publish)
plt.ylabel('R^2 of U', fontdict = font_axis_publish)
plt.xlabel(x_label, fontdict = font_axis_publish)
plt.plot(benchmarking_stats['s2n'],benchmarking_stats['u_r2'])

plt.subplot(1, 2, 2)
plt.title('R^2 score for V', fontdict = font_axis_publish)
plt.ylabel('R^2 of V', fontdict = font_axis_publish)
plt.xlabel(x_label, fontdict = font_axis_publish)
plt.plot(benchmarking_stats['s2n'],benchmarking_stats['v_r2'])

plt.show()