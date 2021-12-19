from openpiv import tools, pyprocess, validation, filters, scaling
import synimagegen as synImg

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# %matplotlib inline

import imageio

# Produce synthetic data parameters
ground_truth,cv,x_1,y_1,U_par,V_par,par_diam1,par_int1,x_2,y_2,par_diam2,par_int2 = synImg.create_synimage_parameters(
  None,[0,1],[0,1],[256,256],dt=0.0025)

frame_a  = synImg.generate_particle_image(256, 256, x_1, y_1, par_diam1, par_int1,16)
frame_b  = synImg.generate_particle_image(256, 256, x_2, y_2, par_diam2, par_int2,16)


sX, sY, sU, sV = ground_truth.create_syn_quiver(4)
print(type(sX), type(sY), type(sU), type(sV))
print(sX.shape, sY.shape, sU.shape, sV.shape)
synData = pd.DataFrame({"x": 256 * sX,"y": 256 * sY, "u": [sU], "v": [sV]})
synData.to_csv('syn_data.csv')
# print(256 * sX, 256 * sY, sU, sV)

winsize = 16 # pixels, interrogation window size in frame A
searchsize = 24  # pixels, search area size in frame B
overlap = 15 # pixels, 50% overlap
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

u1, v1, mask = validation.sig2noise_val(
    u0, v0,
    sig2noise,
    threshold = 1.05,
)

u2, v2 = filters.replace_outliers(
    u1, v1,
    method='localmean',
    max_iter=3,
    kernel_size=3,
)

# convert x,y to mm
# convert u,v to mm/sec

x0, y0, u3, v3 = scaling.uniform(
    x, y, u2, v2,
    scaling_factor = 96.52,  # 96.52 pixels/millimeter
)

# 0,0 shall be bottom left, positive rotation rate is counterclockwise
x1, y1, u4, v4 = tools.transform_coordinates(x, y, u3, v3)

tools.save(x, y, u4, v4, mask, 'OpenPIV_syn_img_pair.txt' )