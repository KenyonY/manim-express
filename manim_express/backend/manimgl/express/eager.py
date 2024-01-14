from ....utils.onlinetex import tex_to_svg_file_online
from ....utils.jupyter import video
from ..scene import SceneGL
from ..config import Size
from .plot import Plot
from .scatter import Scatter

from pathlib import Path
import re
import time
import shutil
from manimlib import (
    BLUE,
    GREEN,
    ShowCreation,
    Write,
    VGroup,
    Transform,
    ReplacementTransform,
    FadeIn,
    FadeOut,
)

from manimlib.utils.rate_functions import linear, smooth
from manimlib.extract_scene import get_scene_config
import manimlib.config
from manimlib.camera.camera import Camera
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
        self._scatter_obj = None

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

    def _play_method(self, mobj, Method, loc):
        loc.pop('self')
        args = loc.pop('args')
        kwargs = loc.pop('kwargs')
        self.play(Method(mobj), *args, **loc, **kwargs)

    def write(self, mobject, *args, run_time=1., rate_func=linear, **kwargs):
        self._play_method(mobject, Write, locals())

    def show_creation(self, mobject, *args, run_time=1, rate_func=linear, **kwargs):
        self._play_method(mobject, ShowCreation, locals())

    def fade_in(self, mobject, *args, run_time=1, rate_func=linear, **kwargs):
        self._play_method(mobject, FadeIn, locals())

    def fade_out(self, mobject, *args, run_time=1, rate_func=linear, **kwargs):
        self._play_method(mobject, FadeOut, locals())

    def get_animate_name_func(self):

        def get_clip_names():
            names = []
            # Fixme: use other method to replace `dir()`
            for name in dir(self):
                if re.search(r'clip_*[0-9]+', name):
                    names.append(name)
            # sort
            if names:
                names = sorted(names, key=lambda x: int(re.search(r"[0-9]+", x).group()))
            return names

        clip_names = get_clip_names()
        animation_func_dict = {}
        if clip_names:
            for func_name in clip_names:
                animation_func_dict.setdefault(func_name, getattr(self, func_name))

        self.animation_func_dict = animation_func_dict

    def save_image(self, filename):
        """This method works only when CONFIG.preview=False. """
        assert (CONFIG.preview == False, "`self.save_image` works only when CONFIG.preview=False.")
        self.camera: Camera
        self.camera.get_image().save(filename)

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
        self.tear_down()

    def tear_down(self):
        super().tear_down()

    def get_config(self):
        return self.config

    def save_default_config(self, config_path=None):
        """Save the default config file to custom directory."""
        if config_path is None:
            shutil.copy(rel_to_abs("custom_config.yml"), 'custom_config.yml')
        else:
            shutil.copy(rel_to_abs("custom_config.yml"), config_path)

    def get_scene_config(self):
        return self.scene_config

    def save_start(self, file_name):
        """TODO"""

    def save_end(self):
        """TODO"""
        # self.file_writer.finish()

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

    def scatter2d(self, x, y, color=BLUE, size=0.05, ax=None, x_range=None, y_range=None, ratio=0.618):
        return self._scatter_nd(x, y, color=color, size=size, ax=ax, x_range=x_range, y_range=y_range, ratio=ratio)

    def scatter3d(self, x, y, z, color=BLUE, size=0.05, ax=None, **kwargs):
        return self._scatter_nd(x, y, z, color=color, size=size, ax=ax, **kwargs)

    def _scatter_nd(self, x, y, z=None, color=BLUE, size=0.05, ax=None, x_range=None, y_range=None, ratio=0.618):
        if self._scatter_obj is None:
            self._scatter_obj = Scatter()

        if ax is not None:
            self._scatter_obj.ax = ax

        if z is not None:
            mobj = self._scatter_obj.from_dot_cloud_3d(
                x, y, z, size=size, color=color, x_range=x_range, y_range=y_range)
        else:
            mobj = self._scatter_obj.from_dotcloud(x, y, size=size, color=color, x_range=x_range, y_range=y_range, ratio=ratio)

        if self._scatter_obj.ax not in self.mobjects:
            self.write(self._scatter_obj.ax)
        self.add(mobj)
        return self._scatter_obj, mobj

    def plot3d(self, x, y, z, width=2, axes_ratio=0.62, show_axes=True):
        """TODO"""

    def get_plot_mobj(self):
        if self.is_axes_line_gen_ed is False:
            self.plt.gen_axes_lines()
        self.is_axes_line_gen_ed = True
        axes_lines_dict = self.plt.get_axes_lines()
        axes_mobj = VGroup(*axes_lines_dict["axes"])
        lines_mobj = VGroup(*axes_lines_dict["line"])
        img = VGroup(axes_mobj, lines_mobj)
        # img.shift(-img.get_center())
        return axes_mobj, lines_mobj

    def get_plot_axes(self):
        return self.plt.get_axes()

    def reset_plot(self):
        self.plt = Plot()
        self.is_axes_line_gen_ed = False

    def show_plot(self, play=True, reset=True):
        axes_mobj, lines_mobj = self.get_plot_mobj()
        pltvgroup = VGroup(axes_mobj, lines_mobj)
        if play:
            self.write(axes_mobj, run_time=1.5, rate_func=smooth)
            self.show_creation(lines_mobj, run_time=1.5, rate_func=smooth)

        else:
            self.add(pltvgroup)
        if reset:
            self.plt = Plot()
        return pltvgroup


class JupyterModeScene(EagerModeScene):
    def __init__(self, write_file=True, **kwargs):
        CONFIG.write_file = write_file
        super().__init__(**kwargs)

    def finish(self):
        self.file_writer.finish()

    def embed(self):
        """We don't need it in jupyter lab/notebook."""

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
