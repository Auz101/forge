"""
Golden capture/compare template for the existing flow (forge build).

Usage (from the repo root, with the project's interpreter):
  GOLDEN_MODE=save    GOLDEN_FILE=<scratchpad>/golden_before.pkl python -m pytest <scratchpad>/test_golden.py -q -p no:cacheprovider --rootdir <scratchpad>
  GOLDEN_MODE=compare GOLDEN_FILE=<scratchpad>/golden_before.pkl python -m pytest <scratchpad>/test_golden.py -q -p no:cacheprovider --rootdir <scratchpad>

- save:    stores the full outputs of each scenario (before the phase's first task).
- compare: compares against what was stored, cell by cell, with no tolerance (after every integration).
It is stored OUTSIDE the repo (scratchpad). Any unexpected difference blocks the task.
"""
import os
import pickle
import sys
from pathlib import Path

import pandas as pd
import pytest

# ---------------------------- ADAPT ------------------------------------------
# 1. Repo path, to import the project's characterization tests.
sys.path.insert(0, r"<REPO_PATH>")

# 2. Reuse the environment fixture (mocked IO, frozen date) and the scenarios
#    from the characterization tests. Example:
#    from tests.test_regression_main_flow import SCENARIOS, run_scenario, env
from tests.test_characterization import SCENARIOS, run_scenario, env  # noqa: F401,E402


def scenario_id(s):
    """Stable, readable identifier of a scenario (key in the golden file)."""
    return str(s[0])


def outputs(env, s):  # noqa: F811
    """
    Runs a scenario and returns a dict with ALL the outputs to pin:
    DataFrames (compared cell by cell) and simple values (subject, recipients, file names).
    """
    return run_scenario(env, s)
# -----------------------------------------------------------------------------

PATH = Path(os.environ["GOLDEN_FILE"])
MODE = os.environ.get("GOLDEN_MODE", "compare")


def _compare(actual, expected, path="root"):
    """Compares recursively: exact DataFrames, dicts by key, everything else by equality."""
    if isinstance(expected, pd.DataFrame):
        pd.testing.assert_frame_equal(actual, expected, check_exact=True, obj=path)
    elif isinstance(expected, dict):
        assert list(actual) == list(expected), f"{path}: keys changed"
        for key in expected:
            _compare(actual[key], expected[key], f"{path}.{key}")
    else:
        assert actual == expected, f"{path}: {actual!r} != {expected!r}"


@pytest.mark.parametrize("s", SCENARIOS, ids=[scenario_id(s) for s in SCENARIOS])
def test_golden(env, s):  # noqa: F811
    actual = outputs(env, s)
    key = scenario_id(s)
    if MODE == "save":
        data = pickle.loads(PATH.read_bytes()) if PATH.exists() else {}
        data[key] = actual
        PATH.write_bytes(pickle.dumps(data))
        return
    _compare(actual, pickle.loads(PATH.read_bytes())[key])
