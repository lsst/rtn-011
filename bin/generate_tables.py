#!/usr/bin/env python
"""Generate all auto-generated LaTeX table files for RTN-011.

Run from the repository root:
    PYTHONPATH=python python bin/generate_tables.py
"""

from pathlib import Path

from lsst.texmf.parameters import RTN011Parameters
from lsst.texmf.tables import (
    make_dp1_fields_table,
    make_dp1_visits_table,
    make_dr_scenario_table,
    make_ops_timeline_table,
    make_pp_scenario_table,
)

TABLES_DIR = Path(__file__).parents[1] / "tables"


def write(path: Path, content: str) -> None:
    path.write_text(content)
    print(f"Written: {path}")


def main() -> None:
    params = RTN011Parameters()
    params.write()

    write(TABLES_DIR / "rubin_ops_timeline.tex",    make_ops_timeline_table(params))
    write(TABLES_DIR / "rubin_early_dr_scenario.tex", make_dr_scenario_table(params))
    write(TABLES_DIR / "rubin_early_pp_scenario.tex", make_pp_scenario_table())
    write(TABLES_DIR / "dp1_fields.tex",            make_dp1_fields_table())
    write(TABLES_DIR / "dp1_fields_visits.tex",     make_dp1_visits_table())


if __name__ == "__main__":
    main()
