import setuptools

setuptools.setup(
    name='simple_static',
    version='0.0.1',
    packages=['simple_static'],
    install_requires=[
        "Jinja2",
        "MarkupSafe",
        "PyYAML",
    ],
    entry_points={
        'console_scripts': [
            'build = simple_static.build:build',
            'serve = simple_static.serve:serve',
        ]
    }
)
