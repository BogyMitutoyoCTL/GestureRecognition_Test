from numpy import interp
import colorsys

"""
TODO: COMMENT
"""

"""
mapHSVTO255
maps a HSV Color from (0-360, 0-100, 0-100) to (0-180, 0-255, 0-255)
"""
def mapHSVTO255(HSVColor):
    h = int(interp(HSVColor[0], [1, 360], [0, 179]))
    s = int(interp(HSVColor[1], [1, 100], [0, 255]))
    v = int(interp(HSVColor[2], [1, 100], [0, 255]))
    return [h, s, v]


def hsv2rgb(h, s, v):
    h = interp(h, [1, 360], [0, 1])
    s = interp(s, [1, 100], [0, 1])
    v = interp(v, [1, 100], [0, 1])
    return tuple(int(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


if __name__ == "__main__":
    print("Nothing to run here. Please run ControllerClass.")
