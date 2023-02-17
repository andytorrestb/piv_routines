from openpiv import tools, pyprocess, validation, filters, scaling
import synimagegen as synImg

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio

import inspect
# Produce synthetic data parameters
ground_truth,cv,x_1,y_1,U_par,V_par,par_diam1,par_int1,x_2,y_2,par_diam2,par_int2 = synImg.create_synimage_parameters(
  None,[-128,128],[-128,128],[800,800],dt=0.0025)

# Produce synthetic data
frame_a  = synImg.generate_particle_image(800, 800, x_1, y_1, par_diam1, par_int1,16)
frame_b  = synImg.generate_particle_image(800, 800, x_2, y_2, par_diam2, par_int2,16)

print(type(frame_a))
input()

sX, sY, sU, sV = ground_truth.create_syn_quiver(25)
print(type(sX), type(sY), type(sU), type(sV))
print(sX.shape, sY.shape, sU.shape, sV.shape)
# print(sX)

# print(ground_truth)
# print(inspect.getmembers(ground_truth))

# for member in inspect.getmembers(ground_truth):
#   print(member)

# Save synthetic data into a format to be saved as a text file. 
synData = pd.DataFrame(columns = ['x', 'y', 'u', 'v'])
synData['x'] = sX.flatten()
synData['y'] = sY.flatten()
synData['u'] = sU.flatten()
synData['v'] = sV.flatten()
synData['flags'] = 0
synData['mask'] = 0
synData.to_csv('ground-truth.txt', index = False)

winsize = 16 # pixels, interrogation window size in frame A
searchsize = 24  # pixels, search area size in frame B
overlap = 12 # pixels, 50% overlap
dt = 0.0025 # sec, time interval between the two frames

u0, v0, sig2noise = pyprocess.extended_search_area_piv(
    frame_a.astype(np.int32),
    frame_b.astype(np.int32),
    window_size=winsize,
    overlap=overlap,
    dt=dt,
    search_area_size=searchsize,
    sig2noise_method='peak2peak',
)

x, y = pyprocess.get_coordinates(
    image_size=frame_a.shape,
    search_area_size=searchsize,
    overlap=overlap,
)

invalid_mask = validation.sig2noise_val(
    sig2noise,
    threshold = 5.0,
)

u2, v2 = filters.replace_outliers(
    u0, v0,
    invalid_mask,
    method='localmean',
    max_iter=3,
    kernel_size=3,
)

# convert x,y to mm
# convert u,v to mm/sec

x0, y0, u3, v3 = scaling.uniform(
    x, y, u2, v2,
    scaling_factor = 1,  # 96.52 pixels/millimeter
)

# 0,0 shall be bottom left, positive rotation rate is counterclockwise
x1, y1, u4, v4 = tools.transform_coordinates(x0, y0, u3, v3)
# x1, y1, u3, v3 = tools.transform_coordinates(x, y, u2, v2)

tools.save('OpenPIV_syn_img_pair-NEW.txt', x1, y1, u4, v4, invalid_mask)

from PIL import Image
im_a = Image.fromarray(frame_a.astype(np.int32))
im_a.save("frame_a.png")

im_b = Image.fromarray(frame_b.astype(np.int32))
im_b.save("frame_b.png")