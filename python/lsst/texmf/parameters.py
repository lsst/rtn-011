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

"""RTN-011 parameter management: load from YAML, write parameters.tex."""

from __future__ import annotations

__all__ = ["RTN011Parameters"]

import subprocess
from pathlib import Path
from typing import Any

import yaml
from astropy.time import Time

from .utils import compute_duration_weeks, is_range, to_long_month_year, to_short_month_year

# Fields in an event dict that are not latex_string: date pairs.
_EVENT_RESERVED = frozenset({
    "key", "name", "description", "date", "latex_string",
    "color", "date_label", "sub_releases",
})

_REPO_ROOT = Path(__file__).parents[3]
DEFAULT_YAML = _REPO_ROOT / "data" / "parameters.yaml"
DEFAULT_TEX = _REPO_ROOT / "parameters.tex"

AUTOGEN_HEADER = """\
%%% This file is auto-generated from data/parameters.yaml -- DO NOT EDIT
%%% Re-generate with: python bin/generate_tables.py
"""


class RTN011Parameters:
    """Milestone and date parameters for RTN-011.

    Loads values from ``data/parameters.yaml`` (sections: ``milestones``,
    ``datarelease``, ``prompt``) and writes ``parameters.tex`` with
    human-readable LaTeX ``\\newcommand`` definitions for all entries.

    Parameters
    ----------
    yaml_path : `~pathlib.Path`, optional
        Path to the parameters YAML file. Defaults to
        ``data/parameters.yaml`` in the repository root.
    """

    def __init__(self, yaml_path: Path = DEFAULT_YAML) -> None:
        with open(yaml_path) as f:
            raw: dict[str, Any] = yaml.safe_load(f)

        # Flat date parameters: {latex_string: iso_value}
        self._dates: dict[str, str] = raw.get("milestones", {})

        # Data release events (may contain sub_releases)
        dr_section = raw.get("datarelease", {})
        self._datarelease: list[dict[str, Any]] = dr_section.get("events", [])

        # Prompt product events
        self._prompt: list[dict[str, Any]] = raw.get("prompt", [])

        # All top-level events combined
        self._events: list[dict[str, Any]] = self._datarelease + self._prompt

        # Combined lookup by latex_string name for __getattr__
        self._by_latexstring: dict[str, str] = dict(self._dates)
        for event in self._events:
            self._by_latexstring[event["latex_string"]] = event["date"]
            for name, value in event.items():
                if name not in _EVENT_RESERVED:
                    self._by_latexstring[name] = value
            for sub in event.get("sub_releases", []):
                self._by_latexstring[sub["latex_string"]] = sub["date"]
                for name, value in sub.items():
                    if name not in _EVENT_RESERVED:
                        self._by_latexstring[name] = value

        # currentdate: YYYY-MM of the most recent git commit (matches vcsDate)
        self._by_latexstring["currentdate"] = self._git_year_month()

        # Derived durations
        self._by_latexstring["durationsvcomcam"] = str(compute_duration_weeks(
            self._by_latexstring["startsvcoomcam"],
            self._by_latexstring["finsvcomcam"],
        )) + " weeks"

    @staticmethod
    def _git_year_month() -> str:
        """Return YYYY-MM of the most recent git commit.

        Matches the vcsDate source used in meta.tex.
        """
        result = subprocess.run(
            ["git", "log", "-1", "--date=short", "--pretty=%ad"],
            capture_output=True, text=True, cwd=_REPO_ROOT,
        )
        return Time(result.stdout.strip(), format="iso", scale="utc").strftime("%Y-%m")

    @property
    def datarelease(self) -> list[dict[str, Any]]:
        """Top-level data release events in YAML order."""
        return self._datarelease

    @property
    def datarelease_expanded(self) -> list[dict[str, Any]]:
        """Data release events with sub_releases flattened.

        Parents that have sub_releases are replaced by their children;
        parents without sub_releases appear directly.
        """
        result = []
        for event in self._datarelease:
            subs = event.get("sub_releases")
            if subs:
                result.extend(subs)
            else:
                result.append(event)
        return result

    @property
    def prompt(self) -> list[dict[str, Any]]:
        """Prompt product events in YAML order."""
        return self._prompt

    @property
    def events(self) -> list[dict[str, Any]]:
        """All top-level events (datarelease + prompt) in YAML order."""
        return self._events

    def __getattr__(self, name: str) -> str:
        try:
            return self._by_latexstring[name]
        except KeyError:
            raise AttributeError(f"No parameter '{name}'") from None

    def __contains__(self, name: str) -> bool:
        """Return True if *name* is a known parameter latex_string."""
        return name in self._by_latexstring

    def _to_display(self, value: str) -> str:
        """Convert an ISO value to a display string for use in LaTeX prose."""
        if value == "TBD":
            return "TBD"
        if is_range(value):
            return to_short_month_year(value)
        if value.count("-") == 1:  # YYYY-MM → long month name
            return to_long_month_year(value)
        if value.count("-") == 2:  # YYYY-MM-DD kept as ISO
            return value
        return value  # non-date strings (e.g. "7 weeks") returned as-is

    def to_latex(self) -> str:
        """Render the full contents of parameters.tex."""
        lines = [AUTOGEN_HEADER]
        for name, value in self._by_latexstring.items():
            if name.startswith("end"):
                raise ValueError(
                    f"Parameter name '{name}' starts with 'end', which is reserved by LaTeX. "
                    "Rename it (e.g. 'fin...' or '...end')."
                )
            if not name.isalpha():
                raise ValueError(
                    f"Parameter name '{name}' contains non-letter characters. "
                    "LaTeX command names may only contain letters."
                )
            display = self._to_display(value)
            lines.append(f"\\newcommand{{\\{name}}}{{{display}\\xspace}}")
        lines.append("")
        return "\n".join(lines)

    def write(self, path: Path | str = DEFAULT_TEX) -> None:
        """Write parameters.tex to *path*."""
        Path(path).write_text(self.to_latex())
        print(f"Written: {path}")
