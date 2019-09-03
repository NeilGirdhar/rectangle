=========
Rectangle
=========
.. image:: https://badge.fury.io/py/rectangle.svg
    :target: https://badge.fury.io/py/rectangle

A class for handling rectangle regions.

Example
=======

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

