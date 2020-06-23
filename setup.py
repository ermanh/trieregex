from os import path
from setuptools import setup, find_packages

from trieregex import __version__


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), 'r') as f:
    readme = f.read()

setup(
    name='trieregex',
    version=__version__,
    description='Build trie-based regular expressions from large word lists',
    long_description=readme,
    author='Herman Leung',
    author_email='leung.hm@gmail.com',
    url='https://github.com/ermanh/trieregex',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.6',
    install_requires=[],
    extras_require={
        'testing': ['pytest']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords=['regular expressions', 'regex', 'pattern', 'trie'],
    license='MIT',
)
