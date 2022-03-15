"""
> source-url: https://stackoverflow.com/questions/29643352/converting-hex-to-rgb-value-in-python

This script contains function that help convert hex color value to and from rgb values

@snip:useful_part

"""

# @begin:useful_part
def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
# @end