"""Small datetime-compatible wrapper for astronomical year numbering.

Python's :mod:`datetime` has no year zero.  The analysis only needs a bounded
Gregorian timeline, so dates are stored internally 2000 years ahead.  The
offset is a multiple of the 400-year Gregorian cycle and therefore preserves
leap days and elapsed-time arithmetic for the supported range.
"""
from datetime import datetime, timedelta
from functools import total_ordering
import re

YEAR_OFFSET = 2000
ISO_RE = re.compile(
    r"^([+-]?\d{4,})-(\d{2})-(\d{2})(?:[ T](\d{2}):(\d{2})(?::(\d{2}))?)?$"
)
HORIZONS_RE = re.compile(
    r"^(b)?(\d+)-([A-Za-z]{3})-(\d{2})\s+(\d{2}):(\d{2}):(\d{2})$",
    re.IGNORECASE,
)
MONTHS = {name.lower(): number for number, name in enumerate(
    ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"), 1
)}
MONTH_NAMES = ("Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")


@total_ordering
class AstroDateTime:
    """Naive UTC date using astronomical years (1 BC == year 0)."""

    __slots__ = ("_value", "_year")

    def __init__(self, year, month, day, hour=0, minute=0, second=0):
        shifted_year = year + YEAR_OFFSET
        if not 1 <= shifted_year <= 9999:
            raise ValueError(f"Astronomical year {year} is outside the supported range")
        self._value = datetime(shifted_year, month, day, hour, minute, second)
        self._year = year

    @property
    def year(self):
        return self._year

    @property
    def month(self):
        return self._value.month

    @property
    def day(self):
        return self._value.day

    @property
    def hour(self):
        return self._value.hour

    @property
    def minute(self):
        return self._value.minute

    @property
    def second(self):
        return self._value.second

    def __hash__(self):
        return hash(self._value)

    def __eq__(self, other):
        return isinstance(other, AstroDateTime) and self._value == other._value

    def __lt__(self, other):
        if not isinstance(other, AstroDateTime):
            return NotImplemented
        return self._value < other._value

    def __sub__(self, other):
        if not isinstance(other, AstroDateTime):
            return NotImplemented
        return self._value - other._value

    def __add__(self, delta):
        if not isinstance(delta, timedelta):
            return NotImplemented
        value = self._value + delta
        return AstroDateTime(value.year - YEAR_OFFSET, value.month, value.day,
                             value.hour, value.minute, value.second)

    def strftime(self, pattern):
        marker = "__ASTRONOMICAL_YEAR__"
        rendered = self._value.strftime(pattern.replace("%Y", marker))
        year = f"{self._year:04d}" if self._year >= 0 else f"-{abs(self._year):04d}"
        return rendered.replace(marker, year)

    def isoformat(self, sep="T"):
        return self.strftime(f"%Y-%m-%d{sep}%H:%M:%S")

    def __str__(self):
        return self.strftime("%Y-%m-%d %H:%M:%S")

    def __repr__(self):
        return f"AstroDateTime({self})"


def parse_iso(value):
    match = ISO_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid astronomical ISO date: {value!r}")
    year, month, day = map(int, match.groups()[:3])
    hour = int(match.group(4) or 0)
    minute = int(match.group(5) or 0)
    second = int(match.group(6) or 0)
    return AstroDateTime(year, month, day, hour, minute, second)


def parse_horizons(value):
    match = HORIZONS_RE.fullmatch(value.strip())
    if not match:
        raise ValueError(f"Invalid Horizons calendar date: {value!r}")
    historical_year = int(match.group(2))
    year = 1 - historical_year if match.group(1) else historical_year
    month = MONTHS[match.group(3).lower()]
    return AstroDateTime(year, month, int(match.group(4)), int(match.group(5)),
                         int(match.group(6)), int(match.group(7)))


def to_horizons(value):
    """Translate astronomical ISO notation to explicit Horizons BC/AD syntax."""
    date = parse_iso(value)
    suffix = (f"-{MONTH_NAMES[date.month - 1]}-{date.day:02d} "
              f"{date.hour:02d}:{date.minute:02d}:{date.second:02d}")
    if date.year <= 0:
        return f"{1 - date.year}bc{suffix}"
    if date.year < 100:
        return f"{date.year}ad{suffix}"
    return f"{date.year:04d}{suffix}"
