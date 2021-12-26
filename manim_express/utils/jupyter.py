# Modified from https://github.com/krassowski/jupyter-manim


import sys
from pathlib import Path
from IPython.core.magic import Magics, magics_class, cell_magic
from IPython.display import HTML

std_out = sys.stdout


def video(path,
          width=854, height=480,
          controls=True, autoplay=True, loop=True):
    return HTML(f"""
    <video
      width="{width}"
      height="{height}"
      autoplay="{'autoplay' if autoplay else ''}"
      {'controls' if controls else ''}
      {'loop' if loop else ''}
    >
        <source src="{path}" type="video/mp4">
    </video>
    """)


def gif(path, width=854, height=480, **kwargs):
    return HTML(f"""
    <img
      width="{width}"
      height="{height}"
      src="{path}"
    >
    """)


def find_ipython_frame(frames):
    for frame in frames:
        if frame.filename.startswith('<ipython-input-'):
            return frame
    return None


class JupyterDisplay(Magics):

    def __init__(self, scene):
        self.jupyter_scene_instance = scene
        self.defaults = {
            'autoplay': True,
            'controls': True,
            'loop': True,
            'remote': False,
            'silent': True,
            'width': 854,
            'height': 480,
            'export_variables': True,
            'is_gif': False
        }

    video_settings = {'width', 'height', 'controls', 'autoplay', 'loop'}
    magic_off_switches = {
        'verbose': 'silent',
        'no-controls': 'controls',
        'no-autoplay': 'autoplay',
        'no-loop': 'loop'
    }

    def display(self):
        # execute the code - won't generate any video, however it will introduce
        # the variables into the notebook's namespace (enabling autocompletion etc);
        # this also allows users to get feedback on some code errors early on

        # path of the output video
        path = self.jupyter_scene_instance.file_writer.__dict__['movie_file_path']
        print("path", path)

        if path:
            path = Path(path)
            assert path.exists()

            # To display a video in Jupyter, we need to have access to it
            # so it has to be within the working tree. The absolute paths
            # are usually outside of the accessible range.
            relative_path = path.relative_to(Path.cwd())

            print(relative_path)
            return video(relative_path)
