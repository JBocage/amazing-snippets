"""
> inspiration-url: https://jakevdp.github.io/PythonDataScienceHandbook/04.12-three-dimensional-plotting.html

This code is taken from the a github project and shows how to make a contour plot and to plot a line on the surface.

The plotting code is

@snip:plot_snip

A result example is given in the following figure.

@img:plot_contour_and_line_output.png

"""

import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator
import numpy as np

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

# Make data.
X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X**2 + Y**2)
Z = np.sin(R)

xline = np.linspace(-3, 0, 100)
yline = np.linspace(4, 0, 100)
zline = np.sin(np.sqrt(xline**2 + yline**2))

# @begin:plot_snip
# Plot the contour and the line.
ax.contour3D(X, Y, Z,
            15,
            cmap = 'binary',
            )
ax.plot3D(xline, yline, zline, linewidth=5, c='b')
# @end

# Customize the z axis.
ax.set_zlim(-1.01, 1.01)
ax.zaxis.set_major_locator(LinearLocator(10))
# A StrMethodFormatter is used automatically
ax.zaxis.set_major_formatter('{x:.02f}')

plt.show()