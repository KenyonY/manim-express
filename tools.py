from sparrow import yaml_load

def update_requirements():
    verson_config = yaml_load('./manimlib/version-config.yaml')
    pkg_name = verson_config.get('name')
    version_str = verson_config.get('version')

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


def update_setup_cfg():
    verson_config = yaml_load('./manim_express/version-config.yaml')
    pkg_name = verson_config.get('name')
    with open('setup.cfg', 'r', encoding='utf8') as fio:
        lines = fio.readlines()
        break_flag = 2
        for idx, line in enumerate(lines.copy()):
            if line[:4] == 'name':
                lines[idx] = f"name = {pkg_name}\n"
                break_flag -= 1
                if break_flag == 0:
                    break
            # elif line[:7] == 'version':
            #     lines[idx] = f"version = {version_str}\n"
            #     break_flag -= 1
            #     if break_flag == 0:
            #         break
    with open('setup.cfg', 'w', encoding='utf8') as fio:
        fio.writelines(lines)





if __name__ == "__main__":
    update_requirements()
