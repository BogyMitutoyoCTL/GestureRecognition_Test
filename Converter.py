from numpy import interp
import colorsys

"""
TODO: COMMENT
"""
def mapHSVTO255(HSVColor):
    H = int(interp(HSVColor[0], [1, 360], [0, 179]))
    S = int(interp(HSVColor[1], [1, 100], [0, 255]))
    V = int(interp(HSVColor[2], [1, 100], [0, 255]))
    return [H, S, V]

def hsv2rgb(h, s, v):
    h = int(interp(h, [1, 360], [0, 1]))
    s = int(interp(s, [1, 100], [0, 1]))
    v = int(interp(v, [1, 100], [0, 1]))
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))