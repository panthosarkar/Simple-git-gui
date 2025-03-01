# setup.py
from setuptools import setup

setup(
    name="simple-git-gui",
    version="0.1.0",
    # We have a single Python file "git_gui.py" living in "src/"
    py_modules=["git_gui"],
    package_dir={"": "src"},
    install_requires=[
        "PyQt6",
        "requests",
        "appdirs",
    ],
    entry_points={
        "gui_scripts": [
            "simple-git-gui = git_gui:main"
        ]
    }
)

