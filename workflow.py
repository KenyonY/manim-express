import os
from sparrow.version_ops import VersionControl
from tools import update_setup_cfg
import time
from git import Repo

pkgname = "manim_express"
pkgdir = pkgname
vc = VersionControl(pkgname, pkgdir)
vc.update_version()
# update_setup_cfg()

vc.update_readme(readme_path="./README.md", license="MIT")
time.sleep(0.1)
vc.update_readme(readme_path="./README_zh.md", license="MIT")

# format code
# os.system("yapf -i -r ./manim_express")

repo = Repo('.')
repo.index.add(["README*.md", "requirements.txt", "workflow.py", "manim_express/version-config.yaml"])
repo.index.commit(f"[Upgrade] Version bump to [{vc.config['version']}]")
repo.create_tag(f"{vc.config['version']}")
remote = repo.remote()
remote.push(f"{vc.config['version']}")
remote.push()
