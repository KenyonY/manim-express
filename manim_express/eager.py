import random
import time
import shutil
# from manimlib.utils.config_ops import digest_config
# from manimlib.scene.scene_file_writer import SceneFileWriter
from manimlib import Scene, Point, Camera, ShowCreation, Write, Color, VGroup
from manimlib.extract_scene import get_scene_config
import manimlib.config
from manimlib.config import Size
from .tools import ppath
from .plot import Plot
from .onlinetex import tex_to_svg_file_online
import manimlib.mobject.svg.tex_mobject

__all__ = ["EagerModeScene", "JupyterModeScene", "Size", "SceneArgs"]


class SceneArgs:
    # write_file = False
    # file_name = None
    # skip_animations = False  # "Save the last frame"
    color = None  # Background color"
    full_screen = False
    gif = False
    resolution = '1920x1080'

    # Render to a movie file with an alpha channel,
    # if transparent is True, .mov file will be generated.
    transparent = False
    save_pngs = False  # Save each frame as a png
    hd = False
    uhd = False
    quiet = True
    open = False  # Automatically open the saved file once its done
    finder = False  # Show the output file in finder
    frame_rate = None
    video_dir = None  # directory to write video
    start_at_animation_number = None
    use_online_tex = False


class EagerModeScene(Scene):
    def __init__(
        self,
        write_file=False,
        file_name=None,
        screen_size=Size.big,
        scene_name='EagerModeScene',
        CONFIG=None,
    ):
        self.CONFIG = CONFIG
        args = manimlib.config.parse_cli()
        args_dict = vars(args)
        args_dict['file'] = None
        args_dict['scene_names'] = scene_name
        args_dict['screen_size'] = screen_size
        for key, value in SceneArgs.__dict__.items():
            args_dict[key] = value

        if write_file is True or SceneArgs.gif is True:
            args_dict['write_file'] = True
            args_dict['file_name'] = file_name
            if SceneArgs.gif is True:
                args_dict["transparent"] = False

        if SceneArgs.use_online_tex:
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

        self.episodes = []
        self.current_episode = 1
        self.current_animation = 0
        self.loop_start_animation = None
        self.pause_start_animation = 0

    def play(self, *args, run_time=1, **kwargs):
        """TODO:"""
        super().play(*args, run_time=run_time, **kwargs)
        self.current_animation += 1

    def hold_on(self):
        """ Equal to self.tear_down(). """
        self.stop_skipping()
        self.file_writer.finish()
        if self.window and self.linger_after_completion:
            self.interact()

    def get_config(self):
        return self.config

    def save_default_config(self):
        """Save the default config file to current directory."""
        shutil.copy(ppath("custom_config.yml"), 'custom_config.yml')

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

    def plot(self,
             x,
             y,
             color=None,
             width=2,
             axes_ratio=0.62,
             show_axes=True,
             include_tip=True,
             x_label='x',
             y_label='y'):
        self.plt.plot(x, y, color, width, axes_ratio, show_axes, include_tip,
                      x_label, y_label)

    def plot3d(self, x, y, z, width=2, axes_ratio=0.62, show_axes=True):
        """TODO"""
        pass

    def get_plot_mobj(self):
        self.plt.gen_axes_lines()
        return self.plt.get_axes_lines()

    def get_plot_axes(self):
        return self.plt.get_axes()

    def show_plot(self, play=True):
        axes_lines_dict = self.get_plot_mobj()

        random.seed(time.time())
        if play:
            def play_func(Func):
                if axes_lines_dict['axes']:
                    self.play(ShowCreation(VGroup(*axes_lines_dict["axes"])),
                              run_time=1)
                self.play(Func(VGroup(*axes_lines_dict["line"])), run_time=1)

            if random.random() > 0.5:
                play_func(Write)
            else:
                play_func(ShowCreation)
        else:
            self.add(VGroup(*axes_lines_dict["line"],
                            *axes_lines_dict["axes"]))

        self.plt = Plot()


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
