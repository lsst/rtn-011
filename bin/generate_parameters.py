#!/usr/bin/env python3
"""Generate parameters.tex from data/parameters.yaml."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "python"))

from lsst.texmf.parameters import RTN011Parameters

if __name__ == "__main__":
    RTN011Parameters().write()
