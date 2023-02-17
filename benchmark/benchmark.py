import pandas as pd
import cv2 as cv

from ParityPlot import parityPlot
import EDA as eda

synGroundTruth = pd.read_csv('ground-truth.txt')
synPIV = pd.read_csv('OpenPIV_syn_img_pair-NEW.txt', delimiter = '\t')

# print(synGroundTruth.columns)
# print(synPIV.columns)

data = {
    'Ground-Truth': synGroundTruth,
    'PIV-Analysis': synPIV
}

eda.histogram_compare(data)
# eda.print_summary_stats(
#     data['Ground-Truth'].drop(['flags', 'mask'], axis = 1),
#     'Ground Truth')


eda.compare_summary_stats(data)
parityPlot(data['Ground-Truth'], data['PIV-Analysis'])
