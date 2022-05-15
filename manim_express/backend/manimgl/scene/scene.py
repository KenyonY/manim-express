import time
import shutil
# from manimlib.scene.scene_file_writer import SceneFileWriter
from manimlib import Scene, Point, Camera, ShowCreation, Write, Color, VGroup, VMobject
from manimlib.utils.rate_functions import linear, smooth
from manimlib.extract_scene import get_scene_config
import manimlib.config
from manimlib.utils.color import rgb_to_hex
import manimlib.mobject.svg.tex_mobject
from pathlib import Path
from manimlib.event_handler.event_type import EventType
from manimlib.event_handler import EVENT_DISPATCHER
from manimlib.logger import log
from manimlib import Text, Triangle, RIGHT, DecimalNumber, DR, UL, GREEN, LEFT, UP, FadeOut, FadeIn, FadeInFromPoint, \
    FlashyFadeIn
import numpy as np


class SceneGL(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.camera: Camera
        self.pause = 0
        self.show_coord = True
        if self.preview:
            global key, Window
            from pyglet.window import key
            from manimlib.window import Window
            self._init_show_coord()

    def _init_show_coord(self):
        self._coord_x = 0
        self._coord_y = 0
        mobj_coord_x = DecimalNumber(self._coord_x).scale(0.7).set_color(GREEN)
        mobj_coord_y = DecimalNumber(self._coord_y).scale(0.7).set_color(GREEN).next_to(mobj_coord_x, RIGHT, buff=0.4)
        self._coord_mobj = VGroup(mobj_coord_x, mobj_coord_y).to_edge(DR, buff=0.5)
        self.screen_DR = self._coord_mobj.get_center()
        mobj_coord_x.add_updater(lambda m: m.set_value(self._coord_x))
        mobj_coord_y.add_updater(lambda m: m.set_value(self._coord_y))
        self._coord_mobj.add_updater(lambda m: m.move_to(self.screen_DR))
        self.play(FadeIn(self._coord_mobj), run_time=0.3)

    def on_mouse_motion(
            self,
            point: np.ndarray,
            d_point: np.ndarray
    ) -> None:
        if self.show_coord:
            self.screen_DR = self.camera.frame.get_corner(DR) + LEFT * 1.5 + UP * 0.5
            self._coord_x, self._coord_y = point[0], point[1]
            super().on_mouse_motion(point, d_point)

    def on_mouse_drag(self, point, d_point, buttons, modifiers):
        self.mouse_drag_point.move_to(point)

        event_data = {"point": point, "d_point": d_point, "buttons": buttons, "modifiers": modifiers}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.MouseDragEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return
        frame = self.camera.frame
        # Left mouse button
        if buttons == 1:
            frame.increment_theta(-d_point[0] * 1.5)
            frame.increment_phi(d_point[1] * 1.5)

        # Right mouse button
        elif buttons == 4:
            shift = -d_point
            shift[0] *= frame.get_width() / 2
            shift[1] *= frame.get_height() / 2
            transform = frame.get_inverse_camera_rotation_matrix()
            shift = np.dot(np.transpose(transform), shift)
            frame.shift(shift)

    def on_mouse_scroll(self, point, offset):
        event_data = {"point": point, "offset": offset}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.MouseScrollEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return

        frame = self.camera.frame
        if self.window.is_key_pressed(key.Z) or self.window.is_key_pressed(key.LCTRL):
            factor = 1 + np.arctan(27 * offset[1])
            frame.scale(1 / factor, about_point=point)
        else:
            transform = frame.get_inverse_camera_rotation_matrix()
            shift = np.dot(np.transpose(transform), offset)
            frame.shift(-100.0 * shift)

    def on_key_press(self, symbol, modifiers):
        try:
            char = chr(symbol)
        except OverflowError:
            log.warning("The value of the pressed key is too large.")
            return

        event_data = {"symbol": symbol, "modifiers": modifiers}
        propagate_event = EVENT_DISPATCHER.dispatch(EventType.KeyPressEvent, **event_data)
        if propagate_event is not None and propagate_event is False:
            return

        if symbol == key.R:
            self.camera.frame.to_default_state()
        if symbol == key.A:
            self.show_coord = self.show_coord ^ 1
            if self.show_coord:
                self._init_show_coord()
            else:
                # Has bug
                self.play(FadeOut(self._coord_mobj), run_time=0.3)

        if symbol == key.GREATER:
            # FIXME: make it work
            self.window.clear()
            self.camera.clear()
            self.camera.capture(*self.mobjects)
            # self.window.swap_buffers()
            self.camera.get_image().show()

        elif symbol in (key.Q, key.TAB, key.ENTER):  # key.APOSTROPHE,
            self.quit_interaction = True

        elif symbol in (key.SPACE, key.LALT, key.RALT):
            self.pause = self.pause ^ 1
            time_pause_start = time.time()
            if self.pause:
                print("\nPausing animation...")
            if not self.pause:
                print("\n Continue")
            while self.pause == 1:
                self.window: Window
                self.window.clear()
                if symbol == key.SPACE:
                    self.camera.clear()
                self.camera.capture(*self.mobjects)
                self.window.swap_buffers()
            time_delta = time.time() - time_pause_start
            self.real_animation_start_time += time_delta

        else:
            self._clip_control(symbol)

    def _clip_control(self, symbol):
        pass
