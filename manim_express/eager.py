import time
import random
import numpy as np
from manimlib import Scene, Point, Camera
from manimlib.utils.config_ops import digest_config
from manimlib.extract_scene import get_scene_config
from manimlib.scene.scene_file_writer import SceneFileWriter
import manimlib.config

from manimlib.config import Size
from manimlib.utils.color import rgb_to_hex

__all__ = ["EagerModeScene", "JupyterModeScene", "Size", "Config"]


class Config:
    color = rgb_to_hex([0.3, 0.4, 0.5])
    full_screen = False
    resolution = '1920x1080'
    transparent = True,
    save_pngs = False,  # Save each frame as a png
    hd = False
    uhd = False


class EagerModeScene(Scene):
    def __init__(
        self,
        write_file=False,
        file_name=None,
        screen_size=Size.medium,
        gif=False,
        scene_name='EagerModeScene',
        Config=Config,
        CONFIG=None,
    ):

        if CONFIG:
            self.CONFIG = CONFIG

        args = manimlib.config.parse_cli()

        args_dict = vars(args)
        args_dict['file'] = None
        args_dict['scene_names'] = scene_name
        # args_dict['full_screen'] = full_screen
        args_dict['screen_size'] = screen_size
        for key, value in Config.__dict__.items():
            print(key, value)
            args_dict[key] = value
        if write_file is True:
            args_dict['write_file'] = True
            args_dict['file_name'] = file_name
            args_dict['gif'] = gif

        self.config = manimlib.config.get_configuration(args)
        self.scene_config = get_scene_config(self.config)

        # super().__init__(**self.scene_config)
        # -------------------------------------------
        digest_config(self, self.scene_config)

        if self.preview:
            from manimlib.window import Window
            self.window = Window(scene=self, **self.window_config)
            self.camera_config["ctx"] = self.window.ctx
        else:
            self.window = None

        self.camera: Camera = self.camera_class(**self.camera_config)
        self.file_writer = SceneFileWriter(self, **self.file_writer_config)
        self.mobjects = []
        self.num_plays = 0
        self.time = 0
        self.skip_time = 0
        self.original_skipping_status = self.skip_animations

        # Items associated with interaction
        self.mouse_point = Point()
        self.mouse_drag_point = Point()

        # Much nicer to work with deterministic scenes
        if self.random_seed is not None:
            random.seed(self.random_seed)
            np.random.seed(self.random_seed)
        # -------------------------------------------

        self.virtual_animation_start_time = 0
        self.real_animation_start_time = time.time()
        self.file_writer.begin()

        self.setup()

    def hold_on(self):
        """ Equal to self.tear_down(). """
        self.stop_skipping()
        self.file_writer.finish()
        if self.window and self.linger_after_completion:
            self.interact()

    def get_config(self):
        return self.config

    def get_scene_config(self):
        return self.scene_config

    def save_start(self, file_name):
        """TODO"""
        pass

    def save_end(self):
        # self.file_writer.finish()
        pass

    def embed(self):
        super().embed()


class JupyterModeScene(EagerModeScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def hold_on(self):
        self.file_writer.finish()

    def embed(self):
        """We don't need it in jupyter lab/notebook."""
        pass

    def quit(self):
        """Please use exit() or quit() in jupyter cell."""
        pass
