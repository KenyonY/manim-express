import numpy as np

from examples.example_imports import *
from manimlib.utils.bezier import inverse_interpolate


scene = EagerModeScene()

brush = ImageMobject("brushes/watercolor/3.png")
brush2 = ImageMobject("brushes/watercolor/BB_BB_watercolor_CS1_2.png")
brush3 = ImageMobject(r"C:\BaiduNetdiskDownload\CODE\manim-kunyuan\data\pic\USST_logo.svg.png")

image = np.asarray(brush.image)
print(np.asarray(brush.image).shape)
h, w = image.shape





x0, y0 = brush.get_corner(UL)[:2]
x1, y1 = brush.get_corner(DR)[:2]
print(x0, y0, "x0 y0")
print(x1, y1, "x1 y1")


scene.add(brush.move_to(LEFT*4))
scene.add(brush2)
scene.add(brush3)






scene.hold_on()
