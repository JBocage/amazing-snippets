"""
> author: JBocage

This snippet provides a function that can be used to get codes of a huge colors dataset.

The available colors are accessible at https://xkcd.com/color/rgb/
"""

def color(colorname):
    import matplotlib.colors as mcl
    return mcl.XKCD_COLORS['xkcd:'+colorname]