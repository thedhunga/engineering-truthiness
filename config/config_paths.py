"""
Public path configuration for Engineering Truthiness experiments.

All experiments run in public mode by default, using synthetic data
or publicly available datasets. No private data or credentials required.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RUN_ID = "public_run"

# Data directories
DATADIR = REPO_ROOT / "data"
OUTDIR = REPO_ROOT / "outputs"

# Ensure output directory exists
OUTDIR.mkdir(parents=True, exist_ok=True)

# Shared output subdirectories (created per-experiment by make_run_dirs)
# These are defaults; each notebook creates its own run-specific dirs.
