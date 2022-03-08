"""
> source-url: https://matplotlib.org/3.5.1/gallery/subplots_axes_and_figures/colorbar_placement.html

This code is taken from the matplotlib website. It clearly demonstrates **how matplotlib handles colorbar adding
on figures**.

_BONUS_: it also shows how to merge axes for colorbar plotting.

A result example is given in the following figure.

@img:color_bar_integration_output.png

"""
import matplotlib.pyplot as plt
import numpy as np

fig, axs = plt.subplots(2, 2)
cmaps = ['RdBu_r', 'viridis']
for col in range(2):
    for row in range(2):
        ax = axs[row, col]
        pcm = ax.pcolormesh(np.random.random((20, 20)) * (col + 1),
                            cmap=cmaps[col])
    fig.colorbar(pcm, ax=axs[:, col], shrink=0.6)
plt.show()