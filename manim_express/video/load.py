import cv2
import pyglet
from pyglet.media import *

video_path = r"C:\BaiduNetdiskDownload\CODE\manim-express\data\video\ParticleMultiRay.mp4"

# fcap = cv2.VideoCapture(video_path)
# w = int(fcap.get(cv2.CAP_PROP_FRAME_WIDTH))
# h = int(fcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# fps = int(fcap.get(cv2.CAP_PROP_FPS))
# fcount = int(fcap.get(cv2.CAP_PROP_FRAME_COUNT))
# for idx in range(fcount):
#     fcap.set(cv2.CAP_PROP_POS_FRAMES, idx)
#     success, frame = fcap.read()
#     # cv2.imshow('emm', frame)
#     # cv2.waitKey(2)
#     print(idx)
