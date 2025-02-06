.. role:: bash(code)
    :language: bash

.. role:: python(code)
    :language: python

.. image:: https://img.shields.io/pypi/v/rectangle
   :target: https://pypi.org/project/rectangle/
   :alt: PyPI - Version
   :align: center
.. image:: https://img.shields.io/badge/version_scheme-EffVer-0097a7
   :alt: EffVer Versioning
   :target: https://jacobtomlinson.dev/effver
.. image:: https://img.shields.io/pypi/pyversions/rectangle
   :alt: PyPI - Python Version
   :align: center

=========
Rectangle
=========

A class for handling rectangle regions.

-------
Example
-------

.. code-block:: python

    In [1]: from rectangle import Rect

    In [2]: r = Rect(mins=[1, 2], maxes=[4, 6])

    In [3]: r
    Out[3]: Rect([1. 2.], [4. 6.])

    In [4]: r + 1
    Out[4]: Rect([2. 3.], [5. 7.])

    In [5]: s = Rect(sizes=[1, 1])

    In [6]: r < s
    Out[6]: False

    In [7]: s <= r
    Out[7]: True

-----------------------
Contribution guidelines
-----------------------

- Conventions: PEP8.

- How to clean the source:

  - :bash:`ruff check .`
  - :bash:`pyright`
  - :bash:`mypy`
  - :bash:`isort .`
  - :bash:`pylint rectangle`
