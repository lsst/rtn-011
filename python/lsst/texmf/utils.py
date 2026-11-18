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
    "parse_range",
    "to_long_month_year",
    "to_month_num",
    "to_short_month_year",
    "to_year",
]

from astropy.time import Time


def is_range(value: str) -> bool:
    """Return True if value is an ISO 8601 interval (contains '/')."""
    return "/" in value


def _to_time(iso: str) -> Time:
    """Parse YYYY-MM or YYYY-MM-DD into a Time object (day defaults to 1)."""
    padded = iso if iso.count("-") == 2 else f"{iso}-01"
    return Time(padded, format="iso", scale="utc")


def _parse_iso_date(iso: str) -> tuple[int, int, int | None]:
    """Parse YYYY-MM or YYYY-MM-DD into (year, month, day_or_None)."""
    has_day = iso.count("-") == 2
    dt = _to_time(iso).datetime
    return dt.year, dt.month, dt.day if has_day else None


def parse_range(value: str) -> tuple[str, str]:
    """Return the (start, end) of an ISO interval.

    For single dates both elements are the same value.
    """
    if is_range(value):
        start, end = value.split("/")
        return start, end
    return value, value


def to_month_num(value: str) -> int | None:
    """Return the month number (1-12) for a single ISO date.

    Returns ``None`` for ranges or ``TBD``.
    """
    if value == "TBD" or is_range(value):
        return None
    return int(_to_time(value).strftime("%m"))


def to_year(value: str) -> int | None:
    """Return the year for a single ISO date; None for ranges or TBD."""
    if value == "TBD" or is_range(value):
        return None
    return int(_to_time(value).strftime("%Y"))


def to_short_month_year(value: str) -> str:
    """Format value as short display string.

    - ``YYYY-MM-DD`` → "D Mon YYYY" (exact date)
    - ``YYYY-MM`` → "Mon YYYY"
    - ``YYYY-MM/YYYY-MM`` → "Mon -- Mon YYYY" (same year) or
      "Mon YYYY -- Mon YYYY" (different years)
    - ``TBD`` → "TBD"
    """
    if value == "TBD":
        return "TBD"
    if not is_range(value):
        t = _to_time(value)
        if value.count("-") == 2:
            return f"{t.datetime.day} {t.strftime('%b')} {t.datetime.year}"
        return t.strftime("%b %Y")
    start, end = parse_range(value)
    ts, te = _to_time(start), _to_time(end)
    s_year, e_year = ts.datetime.year, te.datetime.year
    if s_year == e_year:
        return f"{ts.strftime('%b')} -- {te.strftime('%b')} {s_year}"
    return f"{ts.strftime('%b')} {s_year} -- {te.strftime('%b')} {e_year}"


def to_long_month_year(value: str) -> str:
    """Format value as long display string.

    - ``YYYY-MM-DD`` or ``YYYY-MM`` → "Month YYYY"
    - ``YYYY-MM/YYYY-MM`` → "Month -- Month YYYY" (or cross-year variant)
    - ``TBD`` → "TBD"
    """
    if value == "TBD":
        return "TBD"
    if not is_range(value):
        return _to_time(value).strftime("%B %Y")
    start, end = parse_range(value)
    ts, te = _to_time(start), _to_time(end)
    s_year, e_year = ts.datetime.year, te.datetime.year
    if s_year == e_year:
        return f"{ts.strftime('%B')} -- {te.strftime('%B')} {s_year}"
    return f"{ts.strftime('%B')} {s_year} -- {te.strftime('%B')} {e_year}"


def colored_month_cells(
    value: str,
    year_months: list[tuple[int, list[int]]],
    color: str,
) -> list[str]:
    """Return a list of cell strings, one per shown (year, month) slot.

    Parameters
    ----------
    value : `str`
        ISO 8601 date, date range, or ``"TBD"``.
    year_months : `list` of ``(year, months)``
        Pairs defining which cells exist in the grid.  ``months`` is a
        list of 1-based month numbers shown as columns for that year.
    color : `str`
        LaTeX color name applied to cells matching the date or range.

    Returns
    -------
    cells : `list` [`str`]
        Flat list with one entry per slot defined by *year_months*.
    """
    cells = [""] * sum(len(ms) for _, ms in year_months)

    if value == "TBD":
        return cells

    start, end = parse_range(value)
    s_year, s_month, _ = _parse_iso_date(start)
    e_year, e_month, _ = _parse_iso_date(end)

    idx = 0
    for year, months in year_months:
        for month in months:
            in_range = (
                (year > s_year or (year == s_year and month >= s_month))
                and (year < e_year or (year == e_year and month <= e_month))
            )
            if in_range:
                cells[idx] = f"\\cellcolor{{{color}}}"
            idx += 1

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
    t0 = Time(start, format="iso", scale="utc")
    t1 = Time(end, format="iso", scale="utc")
    return round((t1 - t0).to_value("d") / 7)