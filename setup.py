"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

APP = ['__main__.py']
DATA_FILES = []
OPTIONS = {'argv_emulation': True}

setup(
	name='wifi-analyzer',
    version='0.0.1',
    description='Parse wifi signal analyzer data',
    long_description=readme,
    author='Don R Walsh',
    author_email='donrwalsh@gmail.com',
    url='https://github.com/Donrwalsh/wifi-analyzer',
    license=license,
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
