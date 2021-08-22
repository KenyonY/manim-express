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



if __name__ == "__main__":
    update_requirements()
