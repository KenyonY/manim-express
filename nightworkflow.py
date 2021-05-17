import os
from guang import rm
import time

rm(['build', 'dist', 'eggs','manim_express.egg-info'])
os.system("pip uninstall manim_express -y && python setup_express.py install")
time.sleep(0.1)
rm(['build', 'dist', 'eggs','manim_express.egg-info'])