"""
> source-url: https://matplotlib.org/3.1.1/tutorials/colors/colorbar_only.html

> WARNING : NOT FUNCTIONNAL

This file provides a way to easily build a custom discrete color bar that is usable in matplotlib plots.
"""

####################################################################################
### BEGINNING OF USEFUL PART #######################################################
####################################################################################
import matplotlib.pyplot as plt
import matplotlib as mpl

def color(colorname):
    import matplotlib.colors as mcl
    return mcl.XKCD_COLORS['xkcd:'+colorname]
cmap = mpl.colors.ListedColormap([color('cyan'),
                                  color('lavender'),
                                  color('eggplant'),
                                  color('lime green')])
cmap.set_over(color('eggshell'))
cmap.set_under(color('turquoise'))

bounds = [1, 2, 4, 7, 8]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
####################################################################################
### END OF USEFUL PART##############################################################
####################################################################################

### Example of use case
fig1, ax1 = plt.subplots(figsize=(6, 1))
fig1.subplots_adjust(bottom=0.5)
cb = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
                               norm=norm,
                               boundaries=[0] + bounds + [13],
                               extend='both',
                               ticks=bounds,
                               spacing='proportional',
                               orientation='horizontal')
cb.set_label('Discrete intervals, some other units')
# fig1.show()

import numpy as np

fig2, ax2 = plt.subplots(figsize=(11, 9))

y, x = np.meshgrid(np.linspace(-3, 3, 100), np.linspace(-3, 3, 100))
z = (1 - x / 2. + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2) + 3
z = z[:-1, :-1]
z_min, z_max = -np.abs(z).max(), np.abs(z).max()

c = ax2.pcolormesh(x, y, z, cmap=cmap)
ax2.set_title('pcolormesh')
# set the limits of the plot to the limits of the data
ax2.axis([x.min(), x.max(), y.min(), y.max()])
fig2.colorbar(c, ax=ax2)

plt.show()
