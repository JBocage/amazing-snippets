"""
> author: JBocage

This script aims to provide an efficient tool to design colorbars from screenshots.

A minimal configuration is done in the underlying part.

@snip:config_part

When saving a colorbar, the script also erases the source screenshot.
"""
import os.path
import pathlib
import joblib
import matplotlib.colors as mcl
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d


def color(colorname):
    return mcl.XKCD_COLORS['xkcd:'+colorname]

def hex_to_rgba(value, transparency=0):
    value = value.lstrip('#')
    lv = len(value)
    return [int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3)] + [1-transparency]

plt.ioff()

# @begin:config_part
save_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../custom_bars')))
input_path = pathlib.Path(os.path.abspath(os.path.join(__file__, '../input')))

interpolation_mode='linear'
# @end:config_part

def make_custom_cmap(colorlist,
                     resolution=1000,
                     interp='linear',
                     fname=''):
    if fname:
        print('Processing '+fname)

    cmap_colorlist = []
    # carr = np.array([[e[0]] + hex_to_rgba(color(e[1])) for e in colorlist])
    carr = np.mean(colorlist, axis=0)*255
    interpaxis = np.linspace(0,1,carr.shape[0])
    itrRED = interp1d(interpaxis, carr[:, 0], kind=interp)
    itrGREEN = interp1d(interpaxis, carr[:, 1], kind=interp)
    itrBLUE = interp1d(interpaxis, carr[:, 2], kind=interp)
    itrA = interp1d(interpaxis, carr[:, 3], kind=interp)

    for i, ratio in enumerate(np.linspace(0, 1, resolution)):
        cinterp = [itrRED(ratio),
                   itrGREEN(ratio),
                   itrBLUE(ratio),
                   itrA(ratio)
                   # 1
                   ]
        cmap_colorlist.append(cinterp)

    cm = mcl.ListedColormap(cmap_colorlist)
    fig = plt.figure()
    ax_c = plt.subplot2grid((3, 1), (0,0), rowspan=2, fig=fig)
    ax_cb = plt.subplot2grid((3, 1), (2, 0), fig=fig)
    colors = cm(np.linspace(0, 1, cm.N))

    ax_c.plot([rgba[0]/255*100 for rgba in cmap_colorlist], c='red')
    ax_c.plot([rgba[1]/255*100 for rgba in cmap_colorlist], c='green')
    ax_c.plot([rgba[2]/255*100 for rgba in cmap_colorlist], c='blue')
    ax_cb.imshow([colors[:,:3].astype(int)],
                 extent=[0, 10, 0, 1]
                 )
    ax_c.set_title('Custom cmap result')
    ax_cb.set_xticks([])
    ax_cb.set_yticks([])
    ax_c.set_xticks([])
    ax_c.set_yticks([0,50,100])
    ax_c.set_xlim([0, resolution])
    ax_c.set_ylabel('RGB (%)')

    (x0,_),(x1,y1) = ax_c.get_position().get_points()
    (_,_),(_,y0) = ax_cb.get_position().get_points()

    ax_c.set_position([x0, y0, x1-x0, y1-y0])

    plt.show()


    svnm = input('Enter a save name (enter for cancelling saving) >')
    if svnm:
        save_path.mkdir(exist_ok=True,
                        parents=True)
        joblib.dump(cm, save_path.joinpath(svnm + '.cmap'))
        return True
    else:
        return False

if __name__=='__main__':

    for fname in os.listdir(input_path):
        img = plt.imread(input_path.joinpath(fname))
        if make_custom_cmap(img,
                            fname=fname,
                            interp=interpolation_mode):
            os.remove(input_path.joinpath(fname))
