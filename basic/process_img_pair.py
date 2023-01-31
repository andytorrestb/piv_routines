# Import dependencies. 
from openpiv import tools, pyprocess, validation, filters, scaling
import numpy as np
import matplotlib.pyplot as plt
import imageio
import logging
import os
import process_img_pair_config as config

# =================================================================================
# ||                           Section 0: Configure Logger                       ||
# =================================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(lineno)s:%(message)s')

file_handler = logging.FileHandler('process_img.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


# =================================================================================
# ||                           Section 1: Load Images                            ||
# =================================================================================
path_to_dir = config.IMAGES['path_to_dir']
file_a = config.IMAGES['file_a']
file_b = config.IMAGES['file_b']

# Fix string format for directory if necessary. 
if not path_to_dir[-1] == '/':
    path_to_dir = path_to_dir + '/'
    
# Check if folder contaning images exists.  
if not os.path.exists(path_to_dir):
    logger.error(" " + path_to_dir + ': Path to directory does not exist.')
    exit()

# Check if images to be analyzed exist. 
try:
    frame_a  = tools.imread(path_to_dir + file_a)
except FileNotFoundError:
    logger.error('FileNotFoundError: ' + path_to_dir + file_b + '  is not found')
    exit()
try:
    frame_b  = tools.imread(path_to_dir + file_b)
except FileNotFoundError:
    logger.error('FileNotFoundError: ' + path_to_dir + file_b + '  is not found')
    exit()


# =================================================================================
# ||                           Section 2: Process Images                         ||
# =================================================================================

# PIV Analysis Parameters

# pixels, interrogation window size in frame A
winsize = config.PIV_CROSS_CORR['winsize']

# pixels, search area size in frame B
searchsize = config.PIV_CROSS_CORR['searchsize']

 # pixels, 50% overlap
overlap = config.PIV_CROSS_CORR['overlap']

 # sec, time interval between the two frames
dt =config.PIV_CROSS_CORR['dt']

# Initial processing, returns an initial component calculation 
# and signal to noise ratio for the velocity vector field.
u0, v0, sig2noise = pyprocess.extended_search_area_piv(
    frame_a.astype(np.int32),
    frame_b.astype(np.int32),
    window_size=winsize,
    overlap=overlap,
    dt=dt,
    search_area_size=searchsize,
    sig2noise_method=config.PIV_CROSS_CORR['sig2noise_method'],
)

# Compute the x, y coordinates of the centers of the interrogation windows. 
# Here, the origin (0, 0) is considered the top left corner of the image.
x, y = pyprocess.get_coordinates(
    image_size=frame_a.shape,
    search_area_size=searchsize,
    overlap=overlap,
)

# =================================================================================
# ||                      Section 3: Post-Process PIV Results                    ||
# =================================================================================

# ID false data according to the signal to noise ratio. 
invalid_mask = validation.sig2noise_val(
    sig2noise,
    threshold = config.SIG2NOISE_VAL['threshold'],
)

# Replace outliers with mean data. 
u2, v2 = filters.replace_outliers(
    u0, v0,
    invalid_mask,
    method=config.REPLACE_OUTLIERS['method'],
    max_iter=config.REPLACE_OUTLIERS['max_iter'],
    kernel_size=config.REPLACE_OUTLIERS['kernel_size'],
)

# convert x,y to mm
# convert u,v to mm/sec
x, y, u3, v3 = scaling.uniform(
    x, y, u2, v2,
    scaling_factor = config.SCALE_UNIFORM['scaling_factor'],  # 96.52 pixels/millimeter
)

# 0,0 shall be bottom left, positive rotation rate is counterclockwise
x, y, u3, v3 = tools.transform_coordinates(x, y, u3, v3)

# =================================================================================
# ||                      Section 4: Save and Visualize Results                  ||
# =================================================================================

# Save file names
fname = config.SAVE_RESULTS['fname']
results_txt = fname + '.txt'
results_png = fname + '.png'

# Save results to a text file.
tools.save(results_txt, x, y, u3, v3, invalid_mask)

# Plot results
fig, ax = plt.subplots(figsize=(8,8))
fig, ax = tools.display_vector_field(
    results_txt,
    ax=ax, scaling_factor=96.52,
    scale=config.DISPLAY_RESULTS['scale'], # scale defines here the arrow length
    width=config.DISPLAY_RESULTS['width'], # width is the thickness of the arrow
    on_img=config.DISPLAY_RESULTS['on_img'], # overlay on the image
    image_name=path_to_dir + file_a,
)

# Save plot to as an image file. 
fig.savefig(results_png)