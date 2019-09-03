#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='rectangle',
    version='0.4',
    description='A class for handling rectangle regions.',
    author='Neil Girdhar',
    author_email='mistersheik@gmail.com',
    project_urls={
        "Bug Tracker": "https://github.com/NeilGirdhar/rectangle/issues",
        "Source Code": "https://github.com/NeilGirdhar/rectangle",
    },
    download_url="https://pypi.python.org/pypi/rectangle",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=[],
    install_requires=['numpy>=1.13'],
    python_requires='>=3.7',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
