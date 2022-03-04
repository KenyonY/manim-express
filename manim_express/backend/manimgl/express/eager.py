from ..scene import SceneGL
from ..config import Size
from ....utils.onlinetex import tex_to_svg_file_online
from ....utils.jupyter import video
from .plot import Plot

from pathlib import Path
import random
import time
import shutil
from manimlib import ShowCreation, Write, VGroup
from manimlib.utils.rate_functions import linear, smooth
from manimlib.extract_scene import get_scene_config
import manimlib.config
import os
from sparrow.path import rel_to_abs

__all__ = ["EagerModeScene", "JupyterModeScene", "CONFIG"]


class CONFIG:
    # skip_animations = False  # "Save the last frame"
    color = None  # Background color"
    full_screen = False
    gif = False
    resolution = '1920x1080'
    preview = False
    # Render to a movie file with an alpha channel,
    # if transparent is True, .mov file will be generated.
    transparent = False
    save_pngs = False  # Save each frame as a png
    hd = False
    uhd = False
    quiet = True
    open = False  # Automatically open the saved file once its done
    finder = False  # Show the output file in finder
    frame_rate = 30
    file_name = None
    video_dir = None  # directory to write video
    start_at_animation_number = None
    use_online_tex = False


class EagerModeScene(SceneGL):
    def __init__(
            self,
            screen_size=Size.big,
            scene_name='EagerModeScene',
            # CONFIG=None,
    ):
        # self.CONFIG = CONFIG
        args = manimlib.config.parse_cli()
        args_dict = vars(args)
        args_dict['file'] = None
        args_dict['scene_names'] = scene_name
        args_dict['screen_size'] = screen_size
        if CONFIG.preview:
            from pyglet.window import key
            self.key = key
        else:
            args_dict['write_file'] = True

        for key, value in CONFIG.__dict__.items():
            args_dict[key] = value

        if CONFIG.gif is True:
            args_dict['write_file'] = True
            # if CONFIG.gif is True:
            #     args_dict["transparent"] = False

        if CONFIG.use_online_tex:
            print("Use online latex compiler")
            manimlib.mobject.svg.tex_mobject.tex_to_svg_file = tex_to_svg_file_online

        self.config = manimlib.config.get_configuration(args)
        self.scene_config = get_scene_config(self.config)

        super().__init__(**self.scene_config)

        self.virtual_animation_start_time = 0
        self.real_animation_start_time = time.time()
        self.file_writer.begin()

        self.setup()
        self.plt = Plot()
        self.is_axes_line_gen_ed = False

        self.clips = []
        self.current_clip = 0
        self.saved_states = []
        self.animation_list = []
        self.animation_func_dict = {}
        self.loop_start_animation = None
        self.pause_start_animation = 0

    def play(self, *args, run_time=1, rate_func=linear, **kwargs):
        """TODO:"""
        super().play(*args, run_time=run_time,
                     rate_func=rate_func,
                     **kwargs)

    # def clip1(self):
    #     pass

    def get_animate_name_func(self, n=10):
        animation_func_dict = {}
        for i in range(n):
            try:
                func_name = f"clip{i}"
                animation_func_dict.setdefault(func_name, getattr(self, func_name))
            except:
                continue
        self.animation_func_dict = animation_func_dict

    def render(self):
        self.get_animate_name_func()
        for name, func in self.animation_func_dict.items():
            self.save_state()
            self.saved_states.append(self.saved_state)
            self.current_clip += 1
            func()
            self.animation_list.append(func)
            self.hold_on()

    def replay(self, animation_index=None):
        if animation_index is None:
            animation_index = self.current_clip
        self.saved_state = self.saved_states[animation_index - 1]
        self.restore()
        self.animation_list[animation_index - 1]()

    def loop_animate(self, animation_index=None, num=10):
        while num:
            num -= 1
            self.replay(animation_index)

    def next_animate(self):
        self.current_clip += 1

    def _clip_control(self, symbol):
        # play preview clip
        if symbol in (self.key.LEFT, self.key.COMMA, self.key.NUM_1, self.key._1):
            self.current_clip -= 1
            try:
                self.replay(self.current_clip)
            except IndexError:
                self.current_clip += 1

        # play next clip
        elif symbol in (self.key.RIGHT, self.key.PERIOD, self.key._3, self.key.NUM_3):
            self.current_clip += 1
            try:
                self.replay(self.current_clip)
            except IndexError:
                self.current_clip -= 1

        # play current clip
        elif symbol in (self.key.NUM_DIVIDE, self.key.DOWN, self.key._2, self.key.NUM_2):
            self.replay(self.current_clip)

    def hold_on(self):
        """ Equal to self.tear_down(). """
        self.stop_skipping()
        self.file_writer.finish()
        if self.window and self.linger_after_completion:
            self.interact()

    def tear_down(self):
        super().tear_down()

    def get_config(self):
        return self.config

    def save_default_config(self):
        """Save the default config file to current directory."""
        shutil.copy(rel_to_abs("custom_config.yml"), rel_to_abs('custom_config.yml'))

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

    # FIXME: Remove method `plot` from EagerModeScene.
    def plot(self,
             x,
             y,
             color=None,
             width=2,
             axes_ratio=0.62,
             scale_ratio=None,
             num_decimal_places=None,
             show_axes=True,
             include_tip=True,
             x_label='x',
             y_label='y'):

        """
        params
        ------

        scale_ratio: Scale ratio of coordinate axis. i.e. y / x .
        num_decimal_places: Number of significant digits of coordinate_labels.
        """
        self.plt.plot(x, y, color, width, axes_ratio, scale_ratio, show_axes, include_tip, num_decimal_places,
                      x_label, y_label)

    def plot3d(self, x, y, z, width=2, axes_ratio=0.62, show_axes=True):
        """TODO"""
        pass

    def get_plot_mobj(self):
        if self.is_axes_line_gen_ed is False:
            self.plt.gen_axes_lines()
        self.is_axes_line_gen_ed = True
        axes_lines_dict = self.plt.get_axes_lines()
        axes_mobj = VGroup(*axes_lines_dict["axes"])
        lines_mobj = VGroup(*axes_lines_dict["line"])
        return axes_mobj, lines_mobj

    def get_plot_axes(self):
        return self.plt.get_axes()

    def reset_plot(self):
        self.plt = Plot
        self.is_axes_line_gen_ed = False

    def show_plot(self, play=True, reset=True):
        axes_mobj, lines_mobj = self.get_plot_mobj()
        random.seed(time.time())
        if play:
            def play_func(Func):
                if len(axes_mobj):
                    self.play(ShowCreation(axes_mobj),
                              run_time=1, rate_func=smooth)
                self.play(Func(lines_mobj), run_time=1, rate_func=smooth)

            if random.random() > 0.5:
                play_func(Write)
            else:
                play_func(ShowCreation)
        else:
            self.add(VGroup(axes_mobj,
                            lines_mobj))

        if reset:
            self.plt = Plot()


class JupyterModeScene(EagerModeScene):
    def __init__(self, write_file=True, **kwargs):
        CONFIG.write_file = write_file
        super().__init__(**kwargs)

    def finish(self):
        self.file_writer.finish()

    def embed(self):
        """We don't need it in jupyter lab/notebook."""
        pass

    @property
    def video_path(self):
        path = Path(self.file_writer.get_movie_file_path())
        self.file_writer.finish()
        relative_path = path.relative_to(Path.cwd())
        return str(relative_path)

    def display(self,
                width=854,
                height=480,
                controls=True,
                autoplay=True,
                loop=True):
        return video(self.video_path, width, height, controls, autoplay, loop)

    def quit(self):
        """Please use exit() or quit() in jupyter cell."""
        pass
