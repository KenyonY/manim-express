import os
from sparrow.file_ops import rm
from sparrow.version_ops import VersionControl
from tools import update_requirements

pkgname="manim_express"
pkgdir = pkgname
vc = VersionControl(pkgname, pkgdir)
vc.update_version(1)
# To keep manimlib latest.
update_requirements()
vc.update_readme(license="MIT")


rm('build', 'dist', 'eggs', f'{pkgname}.egg-info')

# os.system("yapf -i -r ./manim_express")
os.system('python setup.py sdist bdist_wheel')
os.system('twine upload dist/*')

rm('build', 'dist', 'eggs', f'{pkgname}.egg-info')

