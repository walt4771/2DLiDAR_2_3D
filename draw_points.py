import time
import matplotlib.pyplot as plt
import math
from time import sleep

x = []
y = []
z = []

import numpy as np

fig = plt.figure()

# fig.canvas.set_window_title('Human Detection Moniter')
lidar_polar = plt.subplot(projection = '3d')

plt.xlabel('x')
plt.ylabel('y')
lidar_polar.set_zlabel('z')

for i in range(0, len(z)):
    z[i] = z[i] if z[i] > 0 else z[i] * -1

for i in range(0, len(y)):
    y[i] = y[i] if y[i] > 0 else y[i] * -1

lidar_polar.scatter(x, y, z, marker=".")
plt.show()
