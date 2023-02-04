import pandas as pd
import cv2 as cv

from ParityPlot import parityPlot
import EDA as eda

synGroundTruth = pd.read_csv('ground-truth.txt')
synPIV = pd.read_csv('OpenPIV_syn_img_pair-NEW.txt', delimiter = '\t')

print(synGroundTruth.columns)
print(synPIV.columns)

titles = ['Ground Truth', 'PIV Analysis']

data = {
    'Ground-Truth': synGroundTruth,
    'PIV-Analysis': synPIV
}

eda.histogram_compare(data)