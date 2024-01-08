# Project Python Cellular Automata

# Python Modules
from setuptools import setup, find_packages

# Local Modules
from pyautomata.version import VERSION

DESCRIPTION = 'Python Cellular Automata',
# LONG_DESCRIPTION = DESCRIPTION

# with open('README.md', 'r', encoding='utf-8') as readme:
#     LONG_DESCRIPTION = readme.read()

setup(
    name='PyAutomata',
    author='Michael Buckley',
    description=DESCRIPTION,
    # long_description=LONG_DESCRIPTION,
    # long_description_content_type = 'text/markdown',
    version=VERSION,
    packages=find_packages(),
    install_requires=[
        'appdirs',
        'numpy',
        'matplotlib'
    ],
    keywords=['cellular automata']
)