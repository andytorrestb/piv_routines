from contour import PivContour
from contour import contour
import matplotlib.pyplot as plt

c = PivContour()

print(c.p)

data = c.load_pandas('test/data/results/test.0000.txt')
fig = plt.figure()

contour(data, c.p, fig)