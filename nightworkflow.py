import os
from guang import rm
os.system("pip uninstall manim_express -y && python setup_express.py install")
rm(['build', 'dist', 'eggs'])