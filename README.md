# Engineering Truthiness

**A Standard for Pseudo–Ground Truth in Machine Learning Evaluation**

[![arXiv](https://img.shields.io/badge/arXiv-forthcoming-b31b1b.svg)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)]()

---

## Overview

This repository contains the reproducible experiments and governance artifacts for:

> **Engineering Truthiness: A Standard for Pseudo–Ground Truth in Machine Learning Evaluation**

Modern ML systems increasingly rely on *silver labels*—proxy-derived supervision from heuristics, weak supervision, similarity measures, or model-assisted annotation—rather than human-verified gold labels. This paper formalizes **engineering truthiness** as a systems-level failure mode in which evaluation results appear sound yet are insufficiently anchored to the latent construct of interest.

We introduce three tools:

| Tool | Purpose |
|------|---------|
| **SILVER** | 6-dimension normative standard for documenting pseudo–ground truth |
| **SEC** | Silver Evaluation Constraints preventing evaluation circularity |
| **SRI** | Silver Risk Index — P(ranking under silver ≠ ranking under gold) |

**Key finding**: Silver labels can support valid evaluation (low SRI) *or* mislead (high SRI)—and the distinction is measurable, not philosophical.

---

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/silver-standard.git
cd silver-standard
pip install -r requirements.txt
```

> **Minimum dependencies** (runs all experiments in synthetic/fallback mode):
> `numpy`, `pandas`, `scikit-learn`, `scipy`, `matplotlib`
>
> **Full dependencies** (uses real IMDB, CIFAR-10, and Snorkel):
> All of the above plus `torch`, `torchvision`, `datasets`, `snorkel`

### 2. Run all experiments

**Option A — Command line** (recommended):

```bash
# Run everything
python run_all.py

# Run only experiments 1 and 3
python run_all.py --experiments 1 3

# Parse-only check (no execution)
python run_all.py --dry-run
```

**Option B — Jupyter notebook:**

```bash
jupyter notebook notebooks/00_run_all.ipynb
```

Open the notebook and run all cells. Set `EXPERIMENTS = [1, 2, 3, 4]` to choose which experiments to include.

**Option C — Google Colab:**

Upload `00_run_all.ipynb` to Colab. It auto-detects the environment and handles paths automatically.

**Option D — Run notebooks individually:**

```bash
jupyter notebook notebooks/01_synthetic_theory_validation.ipynb
```

### 3. Check outputs

All results are saved under `outputs/<experiment_name>/<run_id>/`:

```
outputs/
├── 01_synthetic_theory_validation/
│   └── 01_synthetic_theory_validation_20260303_193619/
│       ├── figures/          # PNG plots
│       ├── tables/           # CSV result tables
│       ├── metrics/
│       ├── logs/
│       └── run_manifest.json # Full run metadata
├── 02_text/
├── 03_clinical/
└── 04_vision/
```

Each run gets a timestamped directory so results are never overwritten.

---

## Automatic Fallbacks

Every notebook detects available dependencies and gracefully degrades:

| Dependency | If missing | Effect on results |
|------------|-----------|-------------------|
| `torch` + `torchvision` | Synthetic CIFAR-10 labels (uniform class distribution) | Same statistical analysis, synthetic data |
| `datasets` | Synthetic text with planted sentiment keywords | Same ranking stability analysis |
| `snorkel` | Simple keyword-voting silver labeler | Same pipeline, simpler proxy |
| Private clinical data | Synthetic patient–trial pairs (200K records) | Same Jaccard analysis, synthetic data |

The core scientific claims (ranking stability under silver evaluation) hold with synthetic data. Full dependencies are needed only to reproduce exact paper figures on real datasets.

---

## Repository Structure

```
silver-standard/
├── run_all.py                            # CLI executor — runs all experiments
├── requirements.txt
├── LICENSE
├── .gitignore
│
├── config/
│   ├── __init__.py
│   ├── config_paths.py                   # Public path defaults
│   └── config_paths_private.py.example   # Template for private data
│
├── notebooks/
│   ├── 00_run_all.ipynb                  # Jupyter executor notebook
│   ├── 01_synthetic_theory_validation.ipynb
│   ├── 02_text_weak_supervision.ipynb
│   ├── 03_clinical_jaccard_fairness.ipynb
│   └── 04_cifar_vision_stress.ipynb
│
├── checklists/
│   ├── SILVER_checklist.md               # SILVER compliance template
│   └── SEC_compliance.md                 # SEC verification template
│
├── docs/
│   └── EXPERIMENTS.md                    # Detailed experiment descriptions
│
└── figures/                              # Generated after running notebooks
```

---

## Experiments

| # | Domain | Paper §  | SRI Regime | Key Demonstration |
|---|--------|----------|-----------|-------------------|
| 1 | Synthetic | 7 | Tunable | Calibration holds while ranking stability fails (Theorem 1) |
| 2 | NLP (IMDB) | 8 | Low | Silver-based model selection is stable |
| 3 | Clinical | 9 | Low | Valid evaluation without gold labels, SILVER-compliant |
| 4 | Vision (CIFAR-10) | 10 | High | Structured noise breaks rankings |

See [`docs/EXPERIMENTS.md`](docs/EXPERIMENTS.md) for detailed descriptions and expected outputs.

---

## Using Private Data

To run with your own clinical data (eICU + ClinicalTrials.gov):

1. Copy the template:
   ```bash
   cp config/config_paths_private.py.example config/config_paths_private.py
   ```
2. Edit `config/config_paths_private.py` with your data paths
3. Re-run — notebooks auto-detect private config

The private config file is gitignored by default.

---

## The SILVER Standard

| Dimension | What to document |
|-----------|-----------------|
| **S** — Source & Provenance | How proxy labels were generated |
| **I** — Intended Claim Scope | What the evaluation can and cannot support |
| **L** — Linkage to Latent Construct | Why the proxy is relevant (or why gold is infeasible) |
| **V** — Validation & Calibration | Stress-testing of proxy behavior |
| **E** — Error Structure & Subgroups | Proxy error across populations |
| **R** — Risk Disclosure | SRI estimate and ranking stability |

Use [`checklists/SILVER_checklist.md`](checklists/SILVER_checklist.md) for your own projects.

---

## Citation

```bibtex
@article{engineering_truthiness_2026,
  title   = {Engineering Truthiness: A Standard for Pseudo--Ground Truth
             in Machine Learning Evaluation},
  author  = {[Author]},
  journal = {arXiv preprint},
  year    = {2026}
}
```

## License

MIT. See [LICENSE](LICENSE).
