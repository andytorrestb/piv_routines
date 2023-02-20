# Andy Torres
# Undergraduate Research Assistant
# Computational Fluids and Aerodynamics Laboratory
# University of Central Florida

# ===================================
# PIV_Routines: automated_study.py ||
# ===================================

'''
Example case to outline the process of benchmarking a PIV analysis. 
This example involves generating synthetic data. Two images are generated, 
where the particles move within the image from frame a to b according to some 
vector field deemed the ground truth. In theory, this should be the 'cleanest' way
to prototype this sort of process. 
'''

# =================================================================================
# ||                         Section 0: Import Relevant Libraries                ||
# =================================================================================

# Standard python utilities.
import logging
import os
import pandas as pd
import numpy as np

# PIV Specific libraries.
from openpiv import tools, pyprocess, validation, filters, scaling

# Locally included Python files.
import synimagegen as synImg
import automated_study_config as config
import study_util as util

# =================================================================================
# ||                         Section 1: Configure Logger                         ||
# =================================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(lineno)s:%(message)s')

file_handler = logging.FileHandler('automated_study.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

logger.info('========================== NEW RUN STARTED ==========================')

# Create directory to store results.
# TO-DO: create unique folder and log file for each run.
results_path = os.getcwd() + '/results'
if not os.path.exists(results_path):
    os.makedirs(results_path)

# =================================================================================
# ||                      Section 2: Load Ground Truth Data                      ||
# =================================================================================

# Load configuration data.
path_to_dir = config.INPUT_DATA['path_to_dir']
file_a = config.INPUT_DATA['file_a']
file_b = config.INPUT_DATA['file_b']
file_results = config.INPUT_DATA['results']

# Fix string format for directory if necessary.
if not path_to_dir[-1] == '/':
    path_to_dir = path_to_dir + '/'

# Check if folder contaning data exists.
if not os.path.exists(path_to_dir):
    logger.error(" " + path_to_dir + ': Path to directory does not exist.')
    exit()

# Check if files for data to be analyzed exists.
# load in data if they do.
try:
    frame_a  = tools.imread(path_to_dir + file_a)
except FileNotFoundError:
    logger.error(' FileNotFoundError: ' + path_to_dir + file_b + '  is not found')
    exit()
try:
    frame_b  = tools.imread(path_to_dir + file_b)
except FileNotFoundError:
    logger.error(' FileNotFoundError: ' + path_to_dir + file_b + '  is not found')
    exit()

try:
    ground_truth  = pd.read_csv(path_to_dir + file_results, sep = '\t',)
except FileNotFoundError:
    logger.error(' FileNotFoundError: ' + path_to_dir + file_results + '  is not found')
    exit()

# Use ground truth data to display and save a vector plot of the solution data.
cff = synImg.continuous_flow_field(ground_truth, inter = True, img = frame_a)
cff.create_syn_quiver(50, path = results_path+'/')

# Log success.
logger.info(' INFO: Succesfully read in ground truth results and images.')

# =================================================================================
# ||                          Section 3: Run PIV Analysis                        ||
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

# Save and display results.
util.save_results(
    results_path,
    x, y, u0, v0,
    path_to_dir,
    file_a, '0'
)

# TO-DO: Report statistical information about the results.

# =================================================================================
# ||                       Section 4: Post-Process PIV Results                   ||
# =================================================================================

# ID false data according to the signal to noise ratio.
invalid_mask = validation.sig2noise_val(
    sig2noise,
    threshold = config.SIG2NOISE_VAL['threshold'],
)

# Replace outliers with mean data.
u1, v1 = filters.replace_outliers(
    u0, v0,
    invalid_mask,
    method=config.REPLACE_OUTLIERS['method'],
    max_iter=config.REPLACE_OUTLIERS['max_iter'],
    kernel_size=config.REPLACE_OUTLIERS['kernel_size'],
)

util.save_results(
    results_path,
    x, y, u1, v1,
    path_to_dir,
    file_a, '1'
)

# convert x,y to mm
# convert u,v to mm/sec
x, y, u2, v2 = scaling.uniform(
    x, y, u1, v1,
    scaling_factor = config.SCALE_UNIFORM['scaling_factor'],  # 96.52 pixels/millimeter
)

# 0,0 shall be bottom left, positive rotation rate is counterclockwise
x, y, u3, v3 = tools.transform_coordinates(x, y, u2, v2)

util.save_results(
    results_path,
    x, y, u2, v2,
    path_to_dir,
    file_a, '2'
)

# =================================================================================
# ||                       Section 5: Data Cleaning of Results                   ||
# =================================================================================

# =================================================================================
# ||                    Section 5: Comparative Analysis of Results               ||
# =================================================================================

# =================================================================================
# ||                   Section 6: Benchmarking Analysis of Results               ||
# =================================================================================