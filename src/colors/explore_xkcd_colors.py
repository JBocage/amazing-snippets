"""
> author: JBocage

This script aims to provide a tool for the user to explore the xkcd color dataset and find the right color that best
fits their expectations.

When running this script, the user is asked to input a color name (see exemple below).

```
Please enter a color name >greenish
```

If the color name is in the skcd color dataset,
the plot is updated to display all the nearest colors in the rgb space that are contained in the xkcd dataset.
Then the script asks for a new color to be entered.

To end the loop, you can type

```
Please enter a color name >stop
```

To stop the process

Exemple output :

@img:explore_xkcd_colors_output.png

"""

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import Rectangle

cell_width = 212
cell_height = 22
margin = 12
topmargin = 40
n_patches = 4 * 5

colors_dict = mcolors.XKCD_COLORS
names = list(colors_dict)

plt.ion()

fig, ax = plt.subplots()

while True:

    color_name = input('Please enter a color name >')
    if color_name=='stop':
        break
    ax.clear()

    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


    def rgb_to_hex(rgb):
        return '#%02x%02x%02x' % rgb

    def rgb_dist(col1, col2):
        r1, g1, b1 = col1
        r2, g2, b2 = col2
        return ((r1-r2)**2 + (g1-g2)**2 + (b1-b2)**2)**.5

    def hex_dist(col1, col2):
        return rgb_dist(hex_to_rgb(col1), hex_to_rgb(col2))

    colors = []
    for n in names:
        colors.append((n[5:], colors_dict[n], hex_dist(colors_dict[n], colors_dict['xkcd:'+color_name])))

    colors.sort(key=lambda x:x[2])
    ncols = 4
    nrows = n_patches // ncols + int(n_patches % ncols > 0)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows-0.5), -cell_height/2.)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title('color exploration: '+color_name, fontsize=24, loc="center", pad=10)

    for i, (name, hex, dist) in enumerate(colors[:n_patches]):
        row = i % nrows + 0.05
        col = i // nrows
        y = row * cell_height

        swatch_width = 0.8*cell_width
        swatch_height = 0.4*cell_height
        swatch_start_x = cell_width * (col+0.1)
        swatch_start_y = y = (row-0.5) * cell_height

        text_pos_x = cell_width * (col+.5)
        text_pos_y = y = (row+.05) * cell_height

        ax.text(text_pos_x, text_pos_y, name, fontsize=10,
                horizontalalignment='center',
                verticalalignment='center')
        ax.text(text_pos_x, text_pos_y+.2*cell_height, hex, fontsize=10,
                horizontalalignment='center',
                verticalalignment='center')

        ax.add_patch(
            Rectangle(xy=(swatch_start_x, swatch_start_y), width=swatch_width,
                      height=swatch_height, facecolor=colors_dict['xkcd:'+name], edgecolor='k',
                      lw=5)
        )

    plt.draw()
    plt.pause(.5)
    plt.show()

plt.ioff()
plt.show()