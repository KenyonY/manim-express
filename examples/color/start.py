from examples.example_imports import *
import colorsys
CONFIG.use_online_tex = True
size=490
im = Image.new("RGB", (size,size))
radius = min(im.size)/2.0
cx, cy = im.size[0]/2, im.size[1]/2
pix = im.load()

for x in range(im.width):
    for y in range(im.height):
        rx = x - cx
        ry = y - cy
        s = (rx ** 2.0 + ry ** 2.0) ** 0.5 / radius
        if s <= 1.0:
            h = ((math.atan2(ry, rx) / math.pi) + 1.0) / 2.0
            rgb = colorsys.hsv_to_rgb(h, s, 1)
            pix[x,y] = tuple([int(round(c*255.0)) for c in rgb])
hsv_hue_sat = im
import matplotlib.pyplot as plt

plt.imshow(im)
plt.show()