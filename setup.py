import setuptools

# read list of dependencies from requirements.txt
with open('requirements.txt', 'r') as f:
    deps = f.read().split("\n")

setuptools.setup(
    name='simple_static',
    version='0.0.1',
    packages=['simple_static'],
    install_requires=deps,
    entry_points={
        'console_scripts': [
            'build = simple_static.build:build',
            'serve = simple_static.serve:serve',
        ]
    }
)
