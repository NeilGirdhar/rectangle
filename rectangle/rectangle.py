from __future__ import annotations

from dataclasses import dataclass
from typing import Any, NoReturn, override

import numpy as np
from numpy.typing import DTypeLike, NDArray

__all__ = ['Rect']


@dataclass  # noqa: PLR0904
class Rect:
    """Rectangle class."""
    data: NDArray[Any]

    @classmethod
    def from_mins_maxes(cls,
                        mins: NDArray[Any],
                        maxes: NDArray[Any],
                        ) -> Rect:
        return Rect(np.stack((mins, maxes)))

    @classmethod
    def from_mins_sizes(cls,
                        mins: NDArray[Any],
                        sizes: NDArray[Any],
                        ) -> Rect:
        return Rect(np.stack((mins, mins + sizes)))

    @classmethod
    def from_point(cls, point: NDArray[Any]) -> Rect:
        return cls.from_mins_maxes(point, point)

    def transformed(self, t: NDArray[Any]) -> Rect:
        """Transform an m-dimensional Rect using a matrix t.

        Args:
            t: An nxn matrix that can transform vectors in the form: [x, y, z, …, 1]. The Rect is
               padded to n dimensions.
        """
        assert t.shape[0] == t.shape[1]
        extra_dimensions = t.shape[0] - self.dimensions - 1

        def transform(a: NDArray[Any]) -> NDArray[Any]:
            return t.dot(np.concatenate((a, [0] * extra_dimensions, [1]),
                                        axis=0
                                        ))[:self.dimensions]
        return Rect.from_mins_maxes(transform(self.mins), transform(self.maxes))

    def bordered(self, border: float | NDArray[Any]) -> Rect:
        """Return a rect that is expanded in all directions by the border."""
        return Rect.from_mins_maxes(self.mins - border,
                    self.maxes + border)

    def extended_to_integer_coordinates(self) -> Rect:
        """Return a rect that is expanded in all directions by the border."""
        return Rect.from_mins_maxes(np.floor(self.mins),
                                    np.ceil(self.maxes))

    def clamp_point(self, point: NDArray[Any]) -> NDArray[Any]:
        """Return the point or rectangle clamped to this rectangle."""
        return np.clip(point, self.mins, self.maxes)

    def clamp_rectangle(self, rect: Rect) -> Rect:
        """Return the point or rectangle clamped to this rectangle."""
        return Rect.from_mins_maxes(np.minimum(self.mins, rect.mins),
                                    np.maximum(self.maxes, rect.maxes))

    def rectified(self) -> Rect:
        """Fixes swaped min-max pairs."""
        return Rect.from_mins_maxes(np.minimum(self.mins, self.maxes),
                    np.maximum(self.maxes, self.mins))

    def astype(self, dtype: DTypeLike) -> Rect:
        return Rect(self.data.astype(dtype))

    def intersection(self, other: Rect, /) -> Rect:
        """Return the largest rectangle that is contained by both rectangles."""
        return Rect.from_mins_maxes(np.maximum(self.mins, other.mins),
                                    np.minimum(self.maxes, other.maxes))

    def union(self, other: Rect, /) -> Rect:
        """Return the smallest rectangle that contains both rectangles."""
        return Rect.from_mins_maxes(np.minimum(self.mins, other.mins),
                    np.maximum(self.maxes, other.maxes))

    def point_union(self, point: NDArray[Any], /) -> Rect:
        """Return the smallest rectangle that contains this rectangle and the point."""
        return Rect.from_mins_maxes(np.minimum(self.mins, point),
                                    np.maximum(self.maxes, point))

    # Properties.
    @property
    def dtype(self) -> DTypeLike:
        return self.data.dtype

    @property
    def dimensions(self) -> int:
        return self.data.shape[1]

    @property
    def center(self) -> NDArray[Any]:
        return (self.mins + self.maxes) / 2

    @property
    def mins(self) -> NDArray[Any]:
        return self.data[0]

    @property
    def maxes(self) -> NDArray[Any]:
        return self.data[1]

    @property
    def sizes(self) -> NDArray[Any]:
        return self.maxes - self.mins

    # Magic methods.
    def __add__(self, other: NDArray[Any]) -> Rect:
        return Rect.from_mins_maxes(self.mins + other, self.maxes + other)

    def __sub__(self, other: NDArray[Any]) -> Rect:
        return Rect.from_mins_maxes(self.mins - other, self.maxes - other)

    def __mul__(self, other: NDArray[Any]) -> Rect:
        return Rect.from_mins_maxes(self.mins * other, self.maxes * other)

    def __truediv__(self, other: NDArray[Any]) -> Rect:
        return Rect.from_mins_maxes(self.mins / other, self.maxes / other)

    def __contains__(self, point_or_rect: Rect | NDArray[Any], /) -> bool:
        if isinstance(point_or_rect, Rect):
            return bool(np.all(point_or_rect.mins >= self.mins and
                               point_or_rect.maxes <= self.maxes))
        return bool(np.all(self.clamp_point(point_or_rect) == point_or_rect))

    def __bool__(self) -> bool:
        return bool(np.all(self.maxes > self.mins))

    @override
    def __repr__(self) -> str:
        return f"Rect({self.mins}, {self.maxes})"

    def __lt__(self, other: Rect) -> bool:
        return bool(np.all(self.maxes < other.mins))

    def __le__(self, other: Rect) -> bool:
        return bool(np.all(self.maxes <= other.mins))

    def __ge__(self, other: Rect) -> bool:
        return bool(np.all(self.mins >= other.maxes))

    def __gt__(self, other: Rect) -> bool:
        return bool(np.all(self.mins > other.maxes))

    @override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Rect):
            raise TypeError
        return bool(np.all(self.data == other.data))

    @override
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, Rect):
            raise TypeError
        return bool(np.any(self.data != other.data))

    @override
    def __hash__(self) -> NoReturn:
        raise RuntimeError
