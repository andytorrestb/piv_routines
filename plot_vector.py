from data_reader import DataReader, contour
from contour import contour
import matplotlib.pyplot as plt

c = DataReader()
data = c.load_pandas('test/data/results/test.0000.txt')
fig = plt.figure()

contour(data, c.p, fig)