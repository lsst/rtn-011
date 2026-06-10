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

"""LaTeX table generators for RTN-011.

Each function returns a complete LaTeX table string and accepts a
``RTN011Parameters`` instance where date-driven content is needed.
Static observational data (field coordinates, visit counts) is embedded
directly in the relevant functions as it is fixed observational record.
"""

from __future__ import annotations

__all__ = [
    "AUTOGEN_STR",
    "make_dp1_fields_table",
    "make_dp1_visits_table",
    "make_dr_scenario_table",
    "make_ops_timeline_table",
    "make_pp_scenario_table",
]

from .parameters import RTN011Parameters
from .utils import colored_month_cells, to_short_month_year

AUTOGEN_STR = "%%% This table is auto-generated from data/parameters.yaml -- DO NOT EDIT"

# ---------------------------------------------------------------------------
# Timeline table
# ---------------------------------------------------------------------------

_TIMELINE_YEARS = (2025, 2026, 2027, 2028)

_MONTH_COL = (
    r"p{1mm} !{\color{gray}\vrule} p{1mm} !{\color{gray}\vrule} p{1mm} !{\color{gray}\vrule}"
    r"p{1mm} !{\color{gray}\vrule} p{1mm} !{\color{gray}\vrule}p{1mm} !{\color{gray}\vrule} "
    r"p{1mm} !{\color{gray}\vrule}p{1mm} !{\color{gray}\vrule} p{1mm} !{\color{gray}\vrule} "
    r"p{1mm} !{\color{gray}\vrule} p{1mm} !{\color{gray}\vrule} p{1mm}|"
)


def _timeline_row(key: str, label: str, value: str, color: str) -> str:
    """Build one data row for the timeline table."""
    start_year = _TIMELINE_YEARS[0]
    end_year   = _TIMELINE_YEARS[-1]
    cells = colored_month_cells(value, start_year, end_year, color)
    display = to_short_month_year(value)

    parts = [f"\\tiny {label} & \\tiny {key} & \\tiny {display}"]
    for yi, year in enumerate(_TIMELINE_YEARS):
        group = cells[yi * 12 : (yi + 1) * 12]
        parts.append("    & " + " & ".join(group) + f"   % {year}")
    return "\n".join(parts)


def make_ops_timeline_table(params: RTN011Parameters) -> str:
    """Generate ``tables/rubin_ops_timeline.tex``."""
    n_years = len(_TIMELINE_YEARS)
    total_cols = 3 + n_years * 12  # 51

    indent = "      "
    col_spec_years = "\n".join(
        f"{indent * (i + 1)}{_MONTH_COL}  % {year}"
        for i, year in enumerate(_TIMELINE_YEARS)
    )

    year_headers = "\n     ".join(
        f"& \\multicolumn{{12}}{{c|}}{{\\textbf{{{year}}}}}"
        for year in _TIMELINE_YEARS
    )

    month_labels_block = "\n".join(
        "        &  " + " & ".join(
            r"\scalebox{.7}  " + m for m in ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"]
        ) + f"    % {year}"
        for year in _TIMELINE_YEARS
    )

    event_rows = []
    for event in params.events:
        if "color" not in event:
            continue
        desc = event["description"].replace("&", r"\&")
        event_rows.append(
            _timeline_row(event["key"], desc, event["date"], event["color"]) + "\n\\\\\\hline"
        )

    rows_str = "\n".join(event_rows)

    return f"""{AUTOGEN_STR}
\\begin{{table}}
\\centering
\\fontsize{{6}}{{10}}\\selectfont
\\setlength{{\\tabcolsep}}{{1.2pt}}
{{\\renewcommand{{\\arraystretch}}{{1.2}}
\\begin{{tabular}}{{|
      @{{\\hspace{{4pt}}}}l@{{\\hspace{{4pt}}}}|@{{\\hspace{{4pt}}}}l@{{\\hspace{{4pt}}}}|@{{\\hspace{{4pt}}}}l@{{\\hspace{{4pt}}}}|
{col_spec_years}
}}

    \\hline
 \\multicolumn{{{total_cols}}}{{|l|}}{{\\fontsize{{9}}{{12}}\\selectfont \\color{{RubinDarkTeal}}\\textbf{{Rubin Operations Survey and Data Release Timeline}}  }}
      \\\\

    \\multicolumn{{{total_cols}}}{{|l|}}{{{{}}}}
     \\\\ \\hline
%
 \\textbf{{Event}} & \\textbf{{Key}}  &  \\textbf{{Date or Range}}
     {year_headers}
           \\\\ \\hline
{rows_str}

% Months annotation
 \\multicolumn{{3}}{{|l|}}{{}}
{month_labels_block}
 \\\\ \\arrayrulecolor{{black}}\\hline\\hline

\\end{{tabular}}}}
\\caption{{Rubin Operations Key Milestones for Early Science}}
\\label{{tab:ops-timeline}}
\\end{{table}}
"""


# ---------------------------------------------------------------------------
# DP1 fields table
# ---------------------------------------------------------------------------

_DP1_FIELDS = [
    ("47 Tuc",          "47 Tuc Globular Cluster",         6.02,   -72.08),
    ("Rubin SV 38 7",   "Low Ecliptic Latitude Field",     37.86,    6.98),
    ("Fornax dSph",     "Fornax Dwarf Spheroidal Galaxy",  40.00,  -34.45),
    ("ECDFS",           "Extended Chandra Deep Field South", 53.13, -28.10),
    ("EDFS",            "Euclid Deep Field South",         59.10,  -48.73),
    ("Rubin SV 95 -25", "Low Galactic Latitude Field",     95.00,  -25.00),
    ("Seagull",         "Seagull Nebula Seagull",         106.23,  -10.51),
]


def make_dp1_fields_table() -> str:
    """Generate ``tables/dp1_fields.tex``."""
    rows = "\n".join(
        f"    {code} & {name}  & {ra:.2f}    & {dec:.2f}    \\\\"
        for code, name, ra, dec in _DP1_FIELDS
    )
    return f"""{AUTOGEN_STR}
\\begin{{table*}}
    \\centering
      \\caption{{ComCam target fields and pointing centers that are to be included in the DP1 dataset. ICRS coordinates are shared in units of decimal degrees.}}
    \\begin{{tabular}}{{@{{}}llcc@{{}}}}
           \\noalign{{\\vspace{{5pt}}}}\\hline\\hline \\noalign{{\\vspace{{5pt}}}}
      \\textbf{{Field Code}} & \\textbf{{ Field Name}}  &\\textbf{{Right Ascension}} & \\textbf{{Declination}} \\\\ \\noalign{{\\vspace{{1pt}}}}
       \\cline{{3-4}}  \\noalign{{\\vspace{{1pt}}}}
    & & \\textit{{deg}} & \\textit{{deg}} \\\\ \\noalign{{\\vspace{{1pt}}}}
    \\hline  \\noalign{{\\vspace{{3pt}}}}
{rows}
     \\noalign{{\\vspace{{3pt}}}}\\hline
    \\end{{tabular}}
    \\label{{tab:dp1_fields}}
\\end{{table*}}"""


# ---------------------------------------------------------------------------
# DP1 visits table
# ---------------------------------------------------------------------------

_DP1_VISITS = [
    ("47 Tuc",            6,   10,  33,  19,   0,   5),
    ("Rubin SV 38 7",     0,   44,  55,  57,  27,   0),
    ("Fornax dSph",       0,    5,  26,  13,   0,   0),
    ("ECDFS",            53,  230, 257, 177, 177,  30),
    ("EDFS ComCam",      20,   61,  90,  42,  42,  20),
    ("Rubin SV 95 -25",  33,   86,  97,  29,  60,  11),
    ("Seagull",          10,   37,  49,   3,  13,   0),
]


def make_dp1_visits_table() -> str:
    """Generate ``tables/dp1_fields_visits.tex``."""
    rows = "\n".join(
        f"    {target:<20} & {u:>6} & {g:>6} & {r:>6} & {i:>6} & {z:>6} & {y:>6} \\\\"
        for target, u, g, r, i, z, y in _DP1_VISITS
    )
    return f"""{AUTOGEN_STR}
\\begin{{table*}}
    \\centering
    \\caption{{Band coverage for seven fields observed during the ComCam on-sky observing campaign that are to be included in the DP1 dataset.}}
    \\begin{{tabular}}{{@{{}}lcccccc@{{}}}}
           \\noalign{{\\vspace{{5pt}}}}\\hline\\hline \\noalign{{\\vspace{{5pt}}}}
    \\textbf{{Target}} & \\textbf{{u}} & \\textbf{{g}} & \\textbf{{r}} & \\textbf{{i}} & \\textbf{{z}} & \\textbf{{y}} \\\\
        \\hline  \\noalign{{\\vspace{{3pt}}}}

{rows}
         \\noalign{{\\vspace{{3pt}}}}\\hline
    \\end{{tabular}}
    \\label{{tab:dp1_fields_visits}}
\\end{{table*}}
"""


# ---------------------------------------------------------------------------
# Data Release scenario table
# ---------------------------------------------------------------------------

# Static dot/dash content per row: (product_label, [dp0.1..dr2])
# _T = confirmed (RubinDarkTeal), _S = stretch (RubinGray1), _X = not available
_T = r"\mycirc[RubinDarkTeal]"
_S = r"\mycirc[RubinGray1]"
_X = "--"

_DR_PRODUCTS = [
    ("Raw Images",
     [_T, _T, _X, _T, _T, _T, _T]),
    (r"DRP Processed  Visit Images  and Source Catalogs",
     [_T, _T, _X, _T, _T, _T, _T]),
    (r"DRP Coadded Images   and Object Catalogs",
     [_T, _T, _X, _T, _T, _T, _T]),
    (r"DRP Cell-based Coadded Images and ShearObject Catalog",
     [_X, _X, _X, _X, _S, _T, _T]),
    (r"DRP ForcedSource Catalogs",
     [_T, _T, _X, _T, _T, _T, _T]),
    (r"DRP Difference Images and DIA Catalogs",
     [_X, _T, _X, _T, _T, _T, _T]),
    (r"DRP SSP Catalogs",
     [_X, _X, _T, _T, _T, _T, _T]),
]


def _dr_date_cell(event: dict) -> str:
    """Date cell string for one DR scenario column header."""
    if "date_label" in event:
        label = event["date_label"]
        if " + " in label:
            prefix, suffix = label.split(" + ", 1)
            return f"\\tiny \\makecell{{ {prefix} \\\\ + {suffix}}}"
        return f"\\tiny \\makecell{{{label}}}"
    date = event["date"]
    if date == "TBD":
        return "\\tiny TBD"
    display = to_short_month_year(date)
    if " -- " in display:
        start_part, end_part = display.split(" -- ", 1)
        return f"\\tiny \\makecell{{ {start_part} --\\\\ {end_part}}}"
    return f"\\tiny {display}"


def _rotated_dataset(description: str) -> str:
    """Rotated makecell for a DR scenario dataset column header.

    The description string is split on whitespace; each word becomes a
    bold line in the rotated cell.
    """
    content = " \\\\\n".join(f"\\textbf{{{word}}}" for word in description.split())
    return f"\\rotatebox[origin=c]{{90}}{{\\tiny\\makecell{{{content}}}}}"


def make_dr_scenario_table(params: RTN011Parameters) -> str:
    """Generate ``tables/rubin_early_dr_scenario.tex``."""
    dr_events = [e for e in params.events if "dataset_description" in e]
    n = len(dr_events)
    total = n + 1  # +1 for the Data Product label column

    date_cells = " & ".join(_dr_date_cell(e) for e in dr_events)
    key_cells = " &  ".join(f"\\textbf{{{e['key']}}}" for e in dr_events)
    dataset_cells = " &\n\t\t".join(_rotated_dataset(e["dataset_description"]) for e in dr_events)
    col_spec = "|l|" + "c|" * n

    rows = []
    for i, (label, dots) in enumerate(_DR_PRODUCTS):
        sep = r" \arrayrulecolor{gray}\hline" if i < len(_DR_PRODUCTS) - 1 else r" \hline"
        row_cells = "   &  ".join(dots)
        rows.append(f"{label}   &   {row_cells} \\\\  {sep}")
    rows_str = "\n".join(rows)

    return f"""{AUTOGEN_STR}
\\begin{{table}}[hbt!]
\\centering
\\fontsize{{6}}{{10}}\\selectfont
\\setlength{{\\tabcolsep}}{{6pt}}
{{\\renewcommand{{\\arraystretch}}{{1.2}}
\\begin{{tabular}}{{{col_spec}}}
    \\hline
\\multicolumn{{{total}}}{{|l|}}{{{{\\fontsize{{9}}{{12}}\\selectfont \\color{{RubinDarkTeal}}\\textbf{{Rubin Early Science -- Data Release Scenario}}}}}}  \\\\\\hline\\hline
\\multirow{{2}}{{*}} {{}} &
        {date_cells}
    \\\\ \\cline{{2-{total}}}

        & {key_cells}
   \\\\\\cline{{2-{total}}}
       \\multirow{{3}}{{*}}{{\\parbox{{0.1\\linewidth}}{{\\vspace{{0.2cm}} \\textbf{{Data Product}}}}}}  &
\t\t{dataset_cells}
    \\\\\\cline{{2-{total} }} \\hline

{rows_str}

 \\arrayrulecolor{{black}}\\hline
\\end{{tabular}}}}
\\caption{{Summary of the main data products expected in each data preview and early LSST data releases. A dark teal dot denotes confirmed data products whereas a gray dot denotes data products that currently remain a stretch goal.}}
\\label{{tab:data-preview-summary}}
\\end{{table}}"""


# ---------------------------------------------------------------------------
# Prompt Products scenario table
# ---------------------------------------------------------------------------

def make_pp_scenario_table() -> str:
    """Generate ``tables/rubin_early_pp_scenario.tex``.

    This table contains predominantly narrative prose; no date parameters
    are used in the cell content.
    """
    return r"""%s
\begin{table}
\centering
\fontsize{6}{10}\selectfont
\setlength{\tabcolsep}{6pt}
{\renewcommand{\arraystretch}{1.3}
    \begin{tabular}{|p{0.31\linewidth} | p{0.32\linewidth}  | p{0.32\linewidth}|}
    \hline
    \multicolumn{3}{|l|}{{\fontsize{9}{12}\selectfont \color{RubinDarkTeal}\textbf{Rubin Early Science -- Alerts \& Prompt Products Scenario}}}  \\\hline\hline


\multirow{1}{*} {}  &
        \tiny  \makecell{Phase 1: 3 -- 16 weeks post Rubin First Light}  &
        \tiny   \makecell{Phase 2: 18 -- 17 weeks post Rubin First Light} \\[5pt] \cline{2-3}
        {\parbox{0.5\linewidth}{\vspace{0.6cm} \textbf{Data Product}}}  &
        { \makecell{ \textbf{LSSTCam Commissioning }  }}  &
        {\makecell{\textbf{Year 1 Survey} \\ \textbf{Operations} }}
         \\[10pt] \cline{2-3} \hline

\textbf{Alerts}     &  Alert volume and latency will improve throughout the commissioning period. Aiming for ``near-live'' brokered Alert stream by the end of LSSTCam Commissioning.  &
Continued ramp up of the alert stream contingent on the availability of templates.  Alerts expected to reach near full volume and fidelity after DR1.  Alert stream latency in year 1 is 120 seconds. \\  \arrayrulecolor{gray}\hline
%%
\textbf{PP Processed Visit Images}     & Commissioning of the PP image differencing and incremental template building. Prompt image release is embargoed during commissioning (\S~\ref{ssec:impact}).  &   Access to processed visit images as prompt products in the first 6 months of the LSST is TBD.      \\  \arrayrulecolor{gray}\hline
\textbf{PP Difference Images}     & Difference imaging will be somewhat limited, since the image template sky coverage will be sparse. Prompt image release is embargoed during commissioning (\S~\ref{ssec:impact}). &     Difference imaging will steadily increase as incremental template building increases the templates available. Access to PP difference images in the first 6 months of LSST is TBD.    \\\hline
%%
\textbf{PP Catalogs}    &   Queryable PPDB available at shared risk. &  PPDB available for query. \\
 (DIASources, DIAObjects, DIAForcedSources)  & & \\\hline
%%
\textbf{PP SSP Catalogs}   &   Measurements of known SSObjects sent to the MPC whenever difference images are available. Searches for new SSObjects performed if appropriately-cadenced data is present. SSP Catalogs likely unavailable for query in the PPDB. &   Standard SSP Daily Data Products produced from difference images as they are available and reported to the MPC. SSP catalogs available for query in the PPDB.  \\  \hline

\arrayrulecolor{black}\hline
\end{tabular}}
\caption{Summary of Prompt data products expected during commissioning and year 1 of survey observations..}
\label{tab:prompt-data-products}
\end{table}
""" % AUTOGEN_STR
