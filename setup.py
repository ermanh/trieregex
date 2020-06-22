from setuptools import setup, find_packages

setup(
    name='trieregex',
    version='1.0.0',
    description='Compose efficient trie-based regexes from large word lists',
    long_description='',
    author='Herman Leung',
    author_email='leung.hm@gmail.com',
    url='https://github.com/ermanh/trieregex',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.6',
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
    keywords=['python', 'regular expressions', 'regex', 'pattern', 'trie'],
    license='MIT',
)
