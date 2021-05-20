
def update_readme():
    pass


def update_requirements(version=None):
    if version is None:
        with open('./manimlib/manimlib/__init__.py', 'r', encoding='utf8') as fi:
            for line in  fi.readlines():
                idx = line.find('__version__')
                if idx != -1:
                    version_str = line.strip('\n').split('=')[1].strip()
                    # version = float(version_str)
                    break
    with open('requirements.txt', 'w', encoding='utf8') as fo:
        fo.write(f"""
        manimlib_kunyuan >= {version_str}
        """)