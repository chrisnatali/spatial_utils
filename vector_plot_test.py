import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import math
import vector
from vector import Vector

def plot_vector(v, axis, color='blue'):
    axis.plot([0, v[0]], [0, v[1]], [0, v[2]], color=color)

fig = plt.figure()
ax = fig.gca(projection='3d')

u = Vector((3, 2, -5))
f = Vector((2, -1, -1))
work_vector = f.dot_onto(u)

plot_vector(f, ax, color='blue')
plot_vector(work_vector, ax, color='green')
plot_vector(u, ax, color='red')

plt.show()


