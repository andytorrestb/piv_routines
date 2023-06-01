from openpiv import tools, pyprocess, validation, filters, scaling
import synimagegen as synImg
import automated_study_config as config

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import imageio

import inspect

# Produce synthetic data parameters
img_h = 800
img_w = 800 
bit_depth = 16

synImg_params = synImg.create_synimage_parameters(
    None,
    [0, img_h],
    [0, img_w],
    [img_h, img_w],
    dt = config.PIV_CROSS_CORR['dt']
)

# Produce synthetic data

frame_a = synImg.generate_particle_image(
    img_h,
    img_w,
    synImg_params['x1'],
    synImg_params['y1'],
    synImg_params['par_diam1'],
    synImg_params['par_int1'],
    bit_depth
)

print(synImg_params['x2'].shape)
print(synImg_params['x1'].shape)

frame_b = synImg.generate_particle_image(
    img_h,
    img_w,
    synImg_params['x2'],
    synImg_params['y2'],
    synImg_params['par_diam2'],
    synImg_params['par_int2'],
    bit_depth
)

print(type(frame_a))

sX, sY, sU, sV = synImg_params['cff'].create_syn_quiver(int(img_h/config.PIV_CROSS_CORR['winsize']))
print(type(sX), type(sY), type(sU), type(sV))
print(sX.shape, sY.shape, sU.shape, sV.shape)
# print(sX)

synImg_params['cff'].save_flow_field('synthetic_data/ground_truth.txt')

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
synData.to_csv('synthetic_data/ground-truth.txt', index = False, sep = '\t')

winsize = 32 # pixels, interrogation window size in frame A
searchsize = int(1.5*winsize)  # pixels, search area size in frame B
overlap = int(0.5*winsize) # pixels, 50% overlap
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
    threshold = 1.05,
)

u2, v2 = filters.replace_outliers(
    u0, v0,
    invalid_mask,
    method='localmean',
    max_iter=3,
    kernel_size=3,
)

# invalid_mask = validation.global_val(
#     u0, v0,
#     (-800, 800),
#     (-800, 800)
# )

# convert x,y to mm
# convert u,v to mm/sec

x0, y0, u3, v3 = scaling.uniform(
    x, y, u2, v2,
    scaling_factor = 1,  # 96.52 pixels/millimeter
)

# 0,0 shall be bottom left, positive rotation rate is counterclockwise
x1, y1, u4, v4 = tools.transform_coordinates(x0, y0, u3, v3)
# x1, y1, u3, v3 = tools.transform_coordinates(x, y, u2, v2)

print(len(x0))
tools.save('OpenPIV_syn_img_pair-NEW.txt', x0, y0, u4, v4, invalid_mask)

from PIL import Image
im_a = Image.fromarray(frame_a.astype(np.int32))
im_a.save("synthetic_data/frame_a.png")

im_b = Image.fromarray(frame_b.astype(np.int32))
im_b.save("synthetic_data/frame_b.png")