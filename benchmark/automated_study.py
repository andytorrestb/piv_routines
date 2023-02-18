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
import logging

# =================================================================================
# ||                         Section 1: Configure Logger                         ||
# =================================================================================
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s:%(name)s:%(lineno)s:%(message)s')

file_handler = logging.FileHandler('automated_study.log')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

print(logger)

# =================================================================================
# ||                      Section 2: Generate Synthetic Data                     ||
# =================================================================================

# =================================================================================
# ||                           Section 3: Process Images                         ||
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
