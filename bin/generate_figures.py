#!/usr/bin/env python
"""Generate all auto-generated LaTeX figure files for RTN-011.

Run from the repository root:
    PYTHONPATH=python python bin/generate_figures.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "python"))

from lsst.texmf.figures import make_dp2_psf_maglim_figure

FIGURES_DIR = Path(__file__).parents[1] / "figures"
FIGURES_DIR.mkdir(exist_ok=True)


def write(path: Path, content: str) -> None:
    path.write_text(content)
    print(f"Written: {path}")


def main() -> None:
    write(FIGURES_DIR / "dp2_psf_maglim.tex", make_dp2_psf_maglim_figure())


if __name__ == "__main__":
    main()
