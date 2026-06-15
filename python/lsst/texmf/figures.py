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

"""RTN-011 auto-generated LaTeX figure environments."""

from __future__ import annotations

__all__ = ["make_dp2_psf_maglim_figure"]

# Filters in display order (3 columns × 2 rows).
_DP2_BANDS = ["u", "g", "r", "i", "z", "y"]

AUTOGEN_HEADER = """\
%%% This file is auto-generated -- DO NOT EDIT
%%% Re-generate with: python bin/generate_figures.py
"""


def make_dp2_psf_maglim_figure() -> str:
    """Return a LaTeX figure environment for the DP2 PSF magnitude-limit maps.

    Produces a 3×2 grid of subfigures (one per band: u, g, r, i, z, y),
    with an overall caption and label.
    """
    cols = 2
    subfig_width = 0.48

    rows: list[list[str]] = []
    for i in range(0, len(_DP2_BANDS), cols):
        rows.append(_DP2_BANDS[i : i + cols])

    subfig_blocks: list[str] = []
    for row_idx, row_bands in enumerate(rows):
        for col_idx, band in enumerate(row_bands):
            subfig = (
                f"    \\begin{{subfigure}}[b]{{{subfig_width}\\textwidth}}\n"
                f"        \\centering\n"
                f"        \\includegraphics[width=\\textwidth]{{dp2_{band}_psf_maglim}}\n"
                f"        \\caption{{${band}$ band}}\n"
                f"        \\label{{fig:dp2_{band}_psf_maglim}}\n"
                f"    \\end{{subfigure}}"
            )
            subfig_blocks.append(subfig)
            if col_idx < len(row_bands) - 1:
                subfig_blocks.append("    \\hfill")
        if row_idx < len(rows) - 1:
            subfig_blocks.append("    \\vspace{0.5em}")

    inner = "\n".join(subfig_blocks)

    caption = (
        "The $5\\sigma$ PSF magnitude limit for point sources across the DP2 footprint, "
        "shown for each of the six LSST bands ($u$, $g$, $r$, $i$, $z$, $y$). "
        "Depth is computed from the coadded images in the DP2 dataset."
    )

    lines = [
        AUTOGEN_HEADER,
        "\\begin{figure*}[htbp]",
        "    \\centering",
        inner,
        f"    \\caption{{{caption}}}",
        "    \\label{fig:dp2_psf_maglim}",
        "\\end{figure*}",
        "",
    ]
    return "\n".join(lines)
