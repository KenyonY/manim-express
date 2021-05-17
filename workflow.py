import os
from guang import rm

rm(['build', 'dist', 'eggs', 'manim_express.egg-info'])

os.system("yapf -i -r ./manim_express")
os.system('python setup_express.py sdist bdist_wheel')
os.system('twine upload dist/*')

rm(['build', 'dist', 'eggs', 'manim_express.egg-info'])