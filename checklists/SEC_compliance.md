# Silver Evaluation Constraints (SEC) — Compliance Verification

**Paper**: Engineering Truthiness: A Standard for Pseudo–Ground Truth in Machine Learning Evaluation

Use this template to verify that an evaluation pipeline satisfies Silver Evaluation Constraints.
SEC prevents evaluation circularity and ensures that silver-based model comparison is scientifically meaningful.

---

## SEC-1: Training–Evaluation Separation

**Requirement**: The proxy mechanism used to generate evaluation labels must not be directly optimized by the model being evaluated.

### Verification Questions

1. What is the proxy mechanism?
   > *(e.g., Jaccard similarity over clinical concept sets)*

2. What does the model learn/optimize?
   > *(e.g., Dense semantic representations via BioBERT cross-encoder)*

3. Can the model reproduce the proxy computation at inference time?
   > [ ] No — the model's architecture and optimization are structurally distinct from the proxy
   > [ ] Yes — SEC-1 is VIOLATED; evaluation may be circular

4. Is self-consistent supervision distinguished from tautological evaluation?
   > *(The proxy defines the task. The model learns to solve the task through a different mechanism. This is self-consistent, not circular.)*

**SEC-1 Status**: [ ] SATISFIED  [ ] VIOLATED  [ ] UNCERTAIN

---

## SEC-2: Proxy Independence

**Requirement**: When multiple proxy signals are available, evaluation should not rely solely on a single mechanism whose biases dominate both training and assessment.

### Verification Questions

1. Are multiple proxy signals available?
   > [ ] Yes → Are they used for cross-validation or stress-testing?
   > [ ] No → Is reliance on a single proxy justified?

2. If a single proxy is used, has it been stress-tested?
   > *(e.g., threshold perturbation, noise injection, alternative similarity measures)*

3. Are known biases of the proxy documented?

**SEC-2 Status**: [ ] SATISFIED  [ ] SATISFIED (with justification)  [ ] VIOLATED

---

## SEC-3: Claim-Proportional Evidence

**Requirement**: The strength of evaluation claims must be proportional to the strength of the proxy.

### Claim Classification

| Claim Type | Supported by Silver? | Notes |
|------------|---------------------|-------|
| Relative model ranking (A > B) | Usually yes, if SRI is low | Core use case |
| Ablation studies | Yes | Same proxy, controlled variation |
| Absolute performance on real task | Requires additional evidence | Silver ≠ gold |
| Individual-level decisions | Generally no | Insufficient for clinical/legal |
| Generalization to new populations | Requires subgroup analysis | Proxy bias may differ |

### Your Claims

1. Claim: _______________
   - Proportional to proxy strength? [ ] Yes  [ ] No
   - Evidence supporting this claim level: _______________

2. Claim: _______________
   - Proportional to proxy strength? [ ] Yes  [ ] No
   - Evidence supporting this claim level: _______________

**SEC-3 Status**: [ ] SATISFIED  [ ] VIOLATED (claims exceed proxy strength)

---

## Overall SEC Status

- [ ] All three SEC constraints satisfied → Evaluation is structurally sound
- [ ] One or more constraints violated → Document violations and remediation plan

**Notes**:
> *(Additional context or remediation plans)*
