from __future__ import annotations

from typing import Optional, Union

import numpy as np

__all__ = ['Rect']


class Rect:

    """
    Rectangle class.
    """

    def __init__(self,
                 mins: Optional[np.ndarray] = None,
                 maxes: Optional[np.ndarray] = None,
                 sizes: Optional[np.ndarray] = None,
                 dimensions: Optional[int] = None,
                 dtype='d'):
        if isinstance(mins, Rect):
            mins = mins
            maxes = maxes
        elif isinstance(mins, np.ndarray) and mins.ndim == 2:
            assert maxes is None
            maxes = mins[1]
            mins = mins[0]
        else:
            if mins is None:
                if sizes is not None and maxes is not None:
                    mins = maxes - sizes
                else:
                    mins = np.zeros(2, dtype=dtype)
            if maxes is None:
                if sizes is not None:
                    maxes = mins + sizes
                else:
                    maxes = mins
        dimensions = dimensions if dimensions is not None else max(len(mins),
                                                                   len(maxes))
        self.data = np.empty((2, dimensions), dtype=dtype)
        self.data[0] = mins[:dimensions]
        self.data[1] = maxes[:dimensions]

    def transformed(self, t) -> Rect:
        """
        Transforms an m-dimensional Rect using t, an nxn matrix that can
        transform vectors in the form: [x, y, z, …, 1].
        The Rect is padded to n dimensions.
        """
        assert t.shape[0] == t.shape[1]
        extra_dimensions = t.shape[0] - self.dimensions - 1

        def transform(a):
            return t.dot(np.concatenate(
                (a, [0] * extra_dimensions, [1]),
                axis=0
            ))[:self.dimensions]
        return Rect(transform(self.mins), transform(self.maxes))

    def bordered(self, border) -> Rect:
        """
        Returns a rect that is expanded in all directions by the border
        """
        return Rect(self.mins - border,
                    self.maxes + border)

    def extended_to_integer_coordinates(self, dtype=None) -> Rect:
        """
        Returns a rect that is expanded in all directions by the border
        """
        return Rect(np.floor(self.mins),
                    np.ceil(self.maxes),
                    dtype=dtype if dtype is not None else self.dtype)

    def clamped(self, point_or_rect: Union[np.ndarray, Rect]) -> Rect:
        """
        Returns the point or rectangle clamped to this rectangle.
        """
        if isinstance(point_or_rect, Rect):
            return Rect(np.minimum(self.mins, point_or_rect.mins),
                        np.maximum(self.maxes, point_or_rect.maxes))
        return np.clip(point_or_rect, self.mins, self.maxes)

    def rectified(self) -> Rect:
        """
        Fixes swaped min-max pairs.
        """
        return Rect(np.minimum(self.mins, self.maxes),
                    np.maximum(self.maxes, self.mins))

    def astype(self, dtype) -> Rect:
        return Rect(self.data.astype(dtype))

    # Properties.
    @property
    def dtype(self):
        return self.data.dtype

    @property
    def dimensions(self):
        return self.data.shape[1]

    @property
    def center(self):
        return (self.mins + self.maxes) / 2

    @property
    def mins(self):
        return self.data[0]

    @property
    def maxes(self):
        return self.data[1]

    @property
    def sizes(self):
        return self.maxes - self.mins

    # Magic methods.
    def __add__(self, other):
        return Rect(self.mins + other, self.maxes + other)

    def __sub__(self, other):
        return Rect(self.mins - other, self.maxes - other)

    def __mul__(self, other):
        return Rect(self.mins * other, self.maxes * other)

    def __div__(self, other):
        return Rect(self.mins / other, self.maxes / other)

    def __contains__(self, point_or_rect):
        if isinstance(point_or_rect, Rect):
            return (not point_or_rect or
                    np.all(point_or_rect.mins >= self.mins and
                           point_or_rect.maxes <= self.maxes))
        return np.all(self.clamped(point_or_rect) == point_or_rect)

    def __and__(self, other):
        """
        Returns the largest rectangle that is contained by both rectangles.
        """
        if other.contains(self):
            return self
        if self.contains(other):
            return other
        if self.contains(other.mins):
            retval = Rect(np.maximum(self.mins, other.mins),
                          np.minimum(self.maxes, other.maxes))
            if retval:
                return retval
        return Rect()

    def __or__(self, point_or_rect):
        """
        Returns the smallest rectangle that contains this rectangle and
        the other point or rectangle.
        """
        if isinstance(point_or_rect, Rect):
            if self and point_or_rect:
                return Rect(np.minimum(self.mins, point_or_rect.mins),
                            np.maximum(self.maxes, point_or_rect.maxes))
            if not self:
                return point_or_rect
            return self
        return Rect(np.minimum(self.mins, point_or_rect),
                    np.maximum(self.maxes, point_or_rect))

    def __bool__(self):
        return bool(np.all(self.maxes > self.mins))

    def __repr__(self):
        return "Rect({}, {})".format(self.mins, self.maxes)

    def __lt__(self, other):
        return np.all(self.maxes < other.mins)

    def __le__(self, other):
        return np.all(self.maxes <= other.mins)

    def __ge__(self, other):
        return np.all(self.mins >= other.maxes)

    def __gt__(self, other):
        return np.all(self.mins > other.maxes)

    def __eq__(self, other):
        return np.all(self.data == other.data)

    def __ne__(self, other):
        return np.any(self.data != other.data)

    def __array__(self):
        """
        Returns a numpy array that can be passed to
        numpy.testing.assert_allclose.
        """
        return self.data
