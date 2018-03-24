#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='rectangle',
    version='0.3',
    description='A class for handling rectangle regions.',
    author='Neil Girdhar',
    author_email='mistersheik@gmail.com',
    url='https://github.com/NeilGirdhar/rectangle',
    download_url='https://github.com/neilgirdhar/rectangle/archive/0.3.tar.gz',
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    keywords=[],
    install_requires=['numpy>=1.13'],
    python_requires='>=3.4'
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
