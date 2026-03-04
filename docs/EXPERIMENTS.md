# Experiment Descriptions

## Cross-Experiment Design Rationale

These four experiments are designed to demonstrate that silver-label evaluation can both succeed and fail, depending on how proxy risk is managed. Together they cover the SILVER framework's key claims:

- **Experiment 1** (Synthetic): Isolates the mathematical phenomenon—ranking instability under structured proxy disagreement—in a controlled setting where ground truth is known. This validates Theorem 1 and calibrates SRI.
- **Experiment 2** (Text/NLP): Tests silver evaluation in a weak supervision pipeline (IMDB sentiment with keyword labeling functions), showing that model selection can be stable under well-behaved proxy error. Complements the WRENCH benchmark findings (Zhang et al., 2021) on evaluation protocol variance.
- **Experiment 3** (Clinical): Applies the full SILVER standard to clinical trial matching with Jaccard-based silver labels, demonstrating SILVER-compliant evaluation in a domain where gold labels are structurally scarce (cf. TREC Clinical Trials Track, 2022; Köpcke et al., 2014).
- **Experiment 4** (Vision): Stress-tests silver evaluation under structured (class-conditional) noise on CIFAR-10, showing that high aggregate agreement can coexist with unstable rankings—the core "engineering truthiness" failure mode.

---

## Experiment 1: Synthetic Double-Noise Validation

**Paper section**: §7
**Notebook**: `01_synthetic_theory_validation.ipynb`
**Dependencies**: numpy, pandas, scikit-learn, matplotlib

### Design

Generates synthetic binary classification data (20,000 samples, 20 features) and applies controlled label noise at rates [0%, 10%, 20%, 30%, 40%]. Trains LogisticRegression models at multiple regularization strengths (C = 0.05 to 10.0) and measures:

1. Gold vs silver test accuracy under increasing noise
2. Pairwise model ranking inversions (rank flips) between gold and silver evaluation

### Expected Outputs

- `fig01_accuracy_vs_noise_mean_std.png`: Gold and silver accuracy converge at low noise, diverge at high noise
- `fig03_pairwise_inversion_rate_mean_std.png`: Ranking flip rate increases with noise—but not monotonically, because structured noise near the decision boundary matters more than aggregate rate
- Summary CSV tables with per-seed results across 20 random seeds

### Connection to Framework

Validates Theorem 1: small localized disagreement can flip rankings even at >90% overall agreement. The pairwise inversion rate directly estimates SRI for this controlled setting.

---

## Experiment 2: Weakly Supervised Text Classification

**Paper section**: §8
**Notebook**: `02_text_weak_supervision.ipynb`
**Dependencies**: numpy, pandas, scikit-learn, matplotlib; optionally datasets, snorkel

### Design

Uses IMDB sentiment classification with keyword-based labeling functions (or Snorkel label model if available). Trains TF-IDF + LogisticRegression with multiple hyperparameter settings and evaluates:

1. Silver vs gold accuracy for each configuration
2. Hyperparameter ranking stability under silver-only evaluation

### Expected Outputs

- `fig01_text_flip_instability.png`: Visualization of ranking stability across hyperparameter configurations
- Per-configuration accuracy table comparing silver and gold evaluation

### Connection to Framework

Demonstrates a **low-SRI regime**: when proxy error is roughly uniform across the label space and not concentrated near decision boundaries, silver evaluation produces stable model rankings. SEC-1 is satisfied because the keyword labeling functions are structurally distinct from the TF-IDF classifier being evaluated.

---

## Experiment 3: Clinical Trial Matching (Jaccard Silver Labels)

**Paper section**: §9
**Notebook**: `03_clinical_jaccard_fairness.ipynb`
**Dependencies**: numpy, pandas, matplotlib; private data optional

### Design

Constructs patient-trial pairs with Jaccard similarity over eligibility criteria as the silver label. Performs:

1. Threshold sweep analysis: how positive-fraction and error rates change with Jaccard threshold τ
2. Subgroup fairness analysis: whether silver-label error rates differ by patient demographics (gender)

### Expected Outputs

- `fig01_tau_vs_posfrac.png`: Threshold sensitivity curve
- `results_03_threshold_sweep_summary.csv`: Per-threshold statistics including α (false positive rate), β (false negative rate), and subgroup fairness gap

### Connection to Framework

Full SILVER compliance demonstration. The Jaccard proxy satisfies SEC-1 (deterministic, not optimized by the models being evaluated) and SEC-2 (proxy generation is independent of model training). The threshold sweep provides the Validation dimension; subgroup analysis provides the Error structure dimension.

---

## Experiment 4: Vision Benchmark Stress Test (CIFAR-10)

**Paper section**: §10
**Notebook**: `04_cifar_vision_stress.ipynb`
**Dependencies**: numpy, pandas, scipy, matplotlib; optionally torch, torchvision

### Design

Applies 20% class-conditional label noise to CIFAR-10 (or synthetic equivalent) and analyzes:

1. Per-class label fidelity (transition matrix between true and silver labels)
2. Subgroup-level (per-class) agreement rates
3. Whether uniform noise produces non-uniform evaluation distortion across classes

### Expected Outputs

- `fig01_cifar_fidelity_by_class.png`: Per-class fidelity visualization
- `results_04_transition_matrix.csv`: Full K×K transition matrix
- `results_04_vision_fidelity.csv`: Per-class agreement statistics

### Connection to Framework

Demonstrates a **high-SRI regime**: even 20% uniform random noise produces non-uniform per-class effects that can destabilize rankings for models with different class-level strengths. This is the "engineering truthiness" failure mode in action—aggregate agreement looks fine, but structured disagreement at the class level breaks model comparison.

---

## Cross-Experiment Synthesis

| Experiment | Domain | SRI Regime | Key Lesson |
|-----------|--------|-----------|------------|
| 1 - Synthetic | Controlled | Tunable | Ranking instability is a mathematical property, not just empirical noise |
| 2 - Text | NLP | Low | Silver evaluation works when proxy error is unstructured and SEC is satisfied |
| 3 - Clinical | Healthcare | Low | SILVER-compliant evaluation is feasible even without gold labels |
| 4 - Vision | CV | High | Aggregate agreement is insufficient; structure of disagreement determines risk |
