import os
from guang import rm
import time
from tools import update_requirements

update_requirements()

rm(['build', 'dist', 'eggs','manim_express.egg-info'])
os.system("pip uninstall manim_express -y && python setup_express.py install")
time.sleep(0.1)
rm(['build', 'dist', 'eggs','manim_express.egg-info'])