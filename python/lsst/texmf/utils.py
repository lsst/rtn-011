# This file is part of RTN-011.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# Use of this source code is governed by a 3-clause BSD-style
# license that can be found in the LICENSE file.

"""Date and range conversion utilities for RTN-011 LaTeX parameters.

All inputs use ISO 8601: YYYY-MM-DD, YYYY-MM, YYYY-MM/YYYY-MM, or "TBD".
"""

__all__ = [
    "colored_month_cells",
    "compute_duration_weeks",
    "is_range",
    "range_end",
    "range_start",
    "to_long_month_year",
    "to_month_num",
    "to_short_month_year",
    "to_year",
]

from datetime import date

_MONTH_SHORT = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
_MONTH_LONG = ["January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"]


def is_range(value: str) -> bool:
    """Return True if value is an ISO 8601 interval (contains '/')."""
    return "/" in value


def _parse_partial(iso: str) -> tuple[int, int, int | None]:
    """Parse YYYY-MM or YYYY-MM-DD into (year, month, day_or_None)."""
    parts = iso.split("-")
    year = int(parts[0])
    month = int(parts[1])
    day = int(parts[2]) if len(parts) == 3 else None
    return year, month, day


def range_start(value: str) -> str:
    """Return the start portion of an ISO interval.

    Single dates are returned unchanged.
    """
    return value.split("/")[0] if is_range(value) else value


def range_end(value: str) -> str:
    """Return the end portion of an ISO interval.

    Single dates are returned unchanged.
    """
    return value.split("/")[1] if is_range(value) else value


def to_month_num(value: str) -> int | None:
    """Return the month number (1-12) for a single ISO date.

    Returns ``None`` for ranges or ``TBD``.
    """
    if value == "TBD" or is_range(value):
        return None
    return _parse_partial(value)[1]


def to_year(value: str) -> int | None:
    """Return the year for a single ISO date; None for ranges or TBD."""
    if value == "TBD" or is_range(value):
        return None
    return _parse_partial(value)[0]


def to_short_month_year(value: str) -> str:
    """Format value as short display string.

    - ``YYYY-MM-DD`` or ``YYYY-MM`` → "Mon YYYY"
    - ``YYYY-MM/YYYY-MM`` → "Mon -- Mon YYYY" (same year) or
      "Mon YYYY -- Mon YYYY" (different years)
    - ``TBD`` → "TBD"
    """
    if value == "TBD":
        return "TBD"
    if is_range(value):
        s_year, s_month, _ = _parse_partial(range_start(value))
        e_year, e_month, _ = _parse_partial(range_end(value))
        s_str = _MONTH_SHORT[s_month - 1]
        e_str = _MONTH_SHORT[e_month - 1]
        if s_year == e_year:
            return f"{s_str} -- {e_str} {s_year}"
        return f"{s_str} {s_year} -- {e_str} {e_year}"
    year, month, _ = _parse_partial(value)
    return f"{_MONTH_SHORT[month - 1]} {year}"


def to_long_month_year(value: str) -> str:
    """Format value as long display string.

    - ``YYYY-MM-DD`` or ``YYYY-MM`` → "Month YYYY"
    - ``YYYY-MM/YYYY-MM`` → "Month -- Month YYYY" (or cross-year variant)
    - ``TBD`` → "TBD"
    """
    if value == "TBD":
        return "TBD"
    if is_range(value):
        s_year, s_month, _ = _parse_partial(range_start(value))
        e_year, e_month, _ = _parse_partial(range_end(value))
        s_str = _MONTH_LONG[s_month - 1]
        e_str = _MONTH_LONG[e_month - 1]
        if s_year == e_year:
            return f"{s_str} -- {e_str} {s_year}"
        return f"{s_str} {s_year} -- {e_str} {e_year}"
    year, month, _ = _parse_partial(value)
    return f"{_MONTH_LONG[month - 1]} {year}"


def colored_month_cells(value: str, start_year: int, end_year: int, color: str) -> list[str]:
    """Return a list of cell strings (one per month) for the timeline grid.

    The list covers start_year January through end_year December.
    Cells for the date or date range carry ``\\cellcolor{color}``; all
    others are empty strings.

    Parameters
    ----------
    value : `str`
        ISO 8601 date, date range, or ``"TBD"``.
    start_year : `int`
        First year of the grid (January of this year is index 0).
    end_year : `int`
        Last year of the grid (December of this year is the final cell).
    color : `str`
        LaTeX color name applied to cells matching the date or range.

    Returns
    -------
    cells : `list` [`str`]
        Flat list of length ``(end_year - start_year + 1) * 12``.
    """
    n_years = end_year - start_year + 1
    cells = [""] * (n_years * 12)

    if value == "TBD":
        return cells

    def _set(year: int, month: int) -> None:
        if start_year <= year <= end_year:
            cells[(year - start_year) * 12 + (month - 1)] = f"\\cellcolor{{{color}}}"

    if is_range(value):
        s_year, s_month, _ = _parse_partial(range_start(value))
        e_year, e_month, _ = _parse_partial(range_end(value))
        for y in range(s_year, e_year + 1):
            m0 = s_month if y == s_year else 1
            m1 = e_month if y == e_year else 12
            for m in range(m0, m1 + 1):
                _set(y, m)
    else:
        year, month, _ = _parse_partial(value)
        _set(year, month)

    return cells


def compute_duration_weeks(start: str, end: str) -> int:
    """Return the number of weeks between two ISO 8601 dates.

    Parameters
    ----------
    start : `str`
        Start date in ``YYYY-MM-DD`` format.
    end : `str`
        End date in ``YYYY-MM-DD`` format.

    Returns
    -------
    weeks : `int`
        Duration rounded to the nearest whole week.
    """
    d0 = date.fromisoformat(start)
    d1 = date.fromisoformat(end)
    return round((d1 - d0).days / 7)
