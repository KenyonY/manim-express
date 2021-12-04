from examples.example_imports import *
import numpy as np
import cv2
from IPython.display import clear_output
from math import atan2

DRAW_YOURSELF = True
TERMS = 350
FRAME_RATE = 30
SECONDS = 60

mouse_held = False
OCV_WIDTH, OCV_HEIGHT = 2000, 2000
ocv_canvas = np.zeros((OCV_HEIGHT, OCV_WIDTH), dtype=np.uint8)
stop_drawing = False


class FCircle():
    @staticmethod
    def exp_nt2pi(n, t):
        return np.exp(n * t * 2 * np.pi * 1j)

    def __init__(self, term, num_terms, target_func, domain):
        self.term = term

        avg = 0
        for time in domain:
            avg += target_func(time) * self.exp_nt2pi(-(term - num_terms), time)
        avg /= domain.size

        self.c = avg
        self.func = lambda t: self.c * self.exp_nt2pi(term - num_terms, t)
        self.radius = ((self.c.real) ** 2 + (self.c.imag) ** 2) ** 0.5

    def set_coors(self, start, color, line_color):
        self.color = color
        self.line_color = line_color
        self.start = start
        self.end = [self.start[0] + self.c.real, self.start[1] + self.c.imag, 0]
        self.mCircle = Circle(color=self.color, radius=self.radius, stroke_width=0.3)
        self.mCircle.move_to(self.start)
        self.arrow = Line(self.start, self.end, color=self.line_color, stroke_width=2)

    def update(self, time):
        val = self.func(time)
        self.end[:] = [self.start[0] + val.real, self.start[1] + val.imag, 0]
        self.mCircle.move_to(self.start)
        self.arrow.set_points_as_corners([self.start, self.end])


class FourierVis(EagerModeScene):
    """
    这里原本继承的是zoomed scene, 但是在最新版本已经移除了这个类
    Removed all functions of GraphScene (moved to once_useful_constructs), MovingCameraScene, ReconfigurableScene, SceneFromVideo, ZoomedScene, and ThreeDScene. Because these can basically be achieved by adjusting CameraFrame (self.camera.frame)
    """
    domain = np.linspace(0, 1, 4000)
    CONFIG = {
        "x_min": -1,
        "x_max": 1,
        "y_min": -1,
        "y_max": 1,
        "always_continually_update": True,
        "zoom_factor": 0.075,
        "zoomed_display_height": 5,
        "zoomed_display_width": 5.5,
        "zoomed_camera_config": {
            "default_frame_stroke_width": 1,
        },
    }

    def get_drawing(self):
        self.drawing = []

        def on_mouse(event, x, y, flags, param):
            global stop_drawing, mouse_held, OCV_HEIGHT, ocv_canvas
            if event == cv2.EVENT_LBUTTONDOWN:
                mouse_held = True
            elif event == cv2.EVENT_LBUTTONUP:
                stop_drawing = True
            if mouse_held and event == cv2.EVENT_MOUSEMOVE:
                if self.drawing and (
                        (y - (OCV_HEIGHT - self.drawing[-1].imag)) ** 2 + (x - self.drawing[-1].real) ** 2) ** 0.5 > 4:
                    cv2.line(ocv_canvas, (x, y), (int(self.drawing[-1].real), OCV_HEIGHT - int(self.drawing[-1].imag)),
                             255)
                    self.drawing.append(complex(x, OCV_HEIGHT - y))
                elif not self.drawing:
                    self.drawing.append(complex(x, OCV_HEIGHT - y))

        cv2.namedWindow('Drawing')
        cv2.setMouseCallback('Drawing', on_mouse)
        while cv2.waitKey(1) & 0xff != ord('q'):
            cv2.imshow('Drawing', ocv_canvas)
            if stop_drawing:
                break
        cv2.destroyWindow('Drawing')

        self.drawing = np.array(self.drawing)
        for arr in self.drawing.real, self.drawing.imag:
            arr -= arr.min()
            arr /= arr.max() / 10
            arr -= 5

    def target_func(self, t):
        if DRAW_YOURSELF:
            return self.drawing[int(t * (len(self.drawing) - 1))]
        return complex(1.4 * 16 / 9 * (((t - 1) * 5 * ((t - 1) + 1) ** 0.5) if t > 0.5 else (-t * 5 * (t + 1) ** 0.5)),
                       (-1 if t < 0.5 else 1) * (np.sin(t * 50) - np.cos(t * 10) - t ** 2 + 0.5 * t ** 3 + 3 * t - 1.5))

    def set_circles(self):
        self.circles = [FCircle(TERMS, TERMS, self.target_func, self.domain)]
        for term in sorted(range(2 * TERMS + 1), key=lambda x: abs(x - TERMS)):
            if term != TERMS:
                self.circles.append(FCircle(term, TERMS, self.target_func, self.domain))

    def sort_circles(self):
        self.circles = sorted(self.circles, key=lambda x: x.radius, reverse=True)
        self.circles[0].set_coors([0, 0, 0], WHITE, WHITE)
        for i in range(1, len(self.circles)):
            color = '#00bfff' if i % 2 else WHITE
            self.circles[i].set_coors(self.circles[i - 1].end, color, WHITE)

    def move_zoomed_camera(self):
        self.camera.frame.move_to([2, 2, 0])

    def clip1(self):
        if DRAW_YOURSELF:
            self.get_drawing()
        self.set_circles()
        print('set circles', end='\t')
        self.sort_circles()
        for circle in self.circles:
            self.add(circle.mCircle, circle.arrow)

        self.zoomed_display.shift(UP * 3.5 + RIGHT * 0.3)
        self.zoomed_camera.frame.set_color(YELLOW)
        self.zoomed_display.display_frame.set_color(YELLOW)
        self.activate_zooming()
        print('creating frames...', end='')
        frames = FRAME_RATE * SECONDS
        frame = 0

        for time in np.linspace(0, 1, frames):
            frame += 1
            if frame % 10:
                clear_output(True)
                print(f'{round(frame / frames * 100, 2)}%')
            loc = self.circles[-1].end.copy()
            for circle in self.circles:
                circle.update(time)

            self.zoomed_camera.frame.move_to(self.circles[-1].end)
            self.add(Line(loc, self.circles[-1].end.copy(), color=RED, stroke_width=3))
            self.wait(1 / FRAME_RATE)


FourierVis().render()
