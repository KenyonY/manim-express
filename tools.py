
def update_requirements(version=None):
    if version is None:
        with open('./manimlib/manimlib/__init__.py', 'r', encoding='utf8') as fi:
            find_flag = 2
            for line in  fi.readlines():
                idx_version = line.find('__version__')
                idx_name = line.find('__name__')
                if idx_version != -1:
                    version_str = line.strip('\n').split('=')[1].strip()
                    # version = float(version_str)
                    find_flag -= 1
                if idx_name != -1:
                    pkg_name = line.strip('\n').split('=')[1].strip().strip("'").strip('"')
                    find_flag -= 1

                if find_flag < 1:
                    break

    with open('requirements.txt', 'w', encoding='utf8') as fo:
        content = f"""
{pkg_name} >= {version_str}
sparrow_tool
fake_headers
requests
# helium
# pyperclip
"""
        fo.write(content)



if __name__ == "__main__":
    update_requirements()
