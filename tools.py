from sparrow import yaml_load


def update_setup_cfg():
    verson_config = yaml_load('./manim_express/version-config.yaml')
    pkg_name = verson_config.get('name')
    with open('setup.cfg', 'r', encoding='utf8') as fio:
        lines = fio.readlines()
        for idx, line in enumerate(lines.copy()):
            if line[:4] == 'name':
                lines[idx] = f"name = {pkg_name}\n"
                break

    with open('setup.cfg', 'w', encoding='utf8') as fio:
        fio.writelines(lines)


if __name__ == "__main__":
    from git import Repo

    # update_requirements()
    repo = Repo()
    # print(repo.git.execute('git status'))
