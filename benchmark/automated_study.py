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

# PIV Specific libraries.
from openpiv import tools

# Locally included Python files.
import synimagegen as synImg
import automated_study_config as config

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

# Log success.
logger.info(' INFO: Succesfully read in ground truth results and images.')

# =================================================================================
# ||                          Section 3: Run PIV Analysis                        ||
# =================================================================================

# =================================================================================
# ||                       Section 4: Post-Process PIV Results                   ||
# =================================================================================

# =================================================================================
# ||                       Section 5: Data Cleaning of Results                   ||
# =================================================================================

# =================================================================================
# ||                    Section 5: Comparative Analysis of Results               ||
# =================================================================================

# =================================================================================
# ||                   Section 6: Benchmarking Analysis of Results               ||
# =================================================================================