import setuptools

setuptools.setup(
    pbr=True,
    package_data={
        "manim_express": [
            '*.yaml', '*.yml',
        ],
    },
)
