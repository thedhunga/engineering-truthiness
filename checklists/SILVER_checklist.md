# SILVER Compliance Checklist

**Paper**: Engineering Truthiness: A Standard for Pseudo–Ground Truth in Machine Learning Evaluation

Use this checklist to document SILVER compliance for any project using silver labels
(pseudo–ground truth) for training or evaluation.

---

## Project Information

- **Project Name**: _______________
- **Date**: _______________
- **Assessor**: _______________
- **Silver Label Type**: _______________  
  *(e.g., Jaccard similarity, weak supervision, LLM-generated, implicit feedback)*

---

## S — Source and Provenance

- [ ] The proxy generation mechanism is explicitly specified
- [ ] All signals used are documented (e.g., structured codes, lexical features, behavioral logs)
- [ ] The algorithmic form is stated (e.g., Jaccard similarity, labeling functions, model predictions)
- [ ] All thresholds, rules, and parameters are recorded
- [ ] The proxy mechanism is reproducible from the documentation alone

**Documentation**:
> *(Describe the proxy generation mechanism here)*

---

## I — Intended Use and Claim Scope

- [ ] The claims supported by silver-based evaluation are explicitly bounded
- [ ] The distinction between ranking claims and absolute performance claims is stated
- [ ] Population-level vs. individual-level applicability is clarified
- [ ] Known limitations of claim scope are disclosed

**Claim Scope Statement**:
> *(State what this evaluation does and does not support)*

---

## L — Linkage to Latent Construct (or Justified Absence)

- [ ] Gold anchors are available and used for calibration, OR
- [ ] The infeasibility of gold labels is explicitly justified
- [ ] Prior literature supporting the proxy's clinical/domain relevance is cited
- [ ] The relationship between proxy and latent construct is characterized

**Linkage Evidence**:
> *(Cite literature, describe gold anchors, or justify absence)*

---

## V — Validation and Calibration

- [ ] Threshold tuning or sensitivity analysis has been performed
- [ ] The proxy has been stress-tested under parameter perturbation
- [ ] Comparison against alternative proxies or baselines is documented
- [ ] Calibration bounds (if applicable) are reported

**Validation Summary**:
> *(Describe calibration evidence)*

---

## E — Error Structure and Subgroup Effects

- [ ] Proxy error rates are assessed across relevant subgroups
- [ ] Demographic, clinical, or contextual stratification is performed where feasible
- [ ] Concentration of proxy error in ranking-critical regions is assessed
- [ ] No subgroup exhibits disproportionate influence on model selection

**Subgroup Analysis**:
> *(Report subgroup error rates and any disparities)*

---

## R — Risk Disclosure

- [ ] Silver Risk Index (SRI) is estimated or bounded
- [ ] The evaluation regime is classified (low/moderate/high SRI)
- [ ] Sensitivity of model rankings to proxy perturbation is assessed
- [ ] Residual risks are disclosed

**SRI Estimate**: _______________  
**Risk Classification**: [ ] Low SRI  [ ] Moderate SRI  [ ] High SRI

**Risk Statement**:
> *(Describe residual risks and their implications for conclusions)*

---

## SEC Compliance

### SEC-1: Training–Evaluation Separation
- [ ] The model does not directly optimize the proxy generation function
- [ ] The model's learned representation is structurally distinct from the proxy mechanism

### SEC-2: Proxy Independence
- [ ] Multiple proxy signals are used where available, OR
- [ ] The reliance on a single proxy is justified and stress-tested

### SEC-3: Claim-Proportional Evidence
- [ ] Evaluation claims are proportional to the strength of the proxy
- [ ] Comparative ranking claims are distinguished from absolute performance claims

---

## Overall Assessment

- [ ] **SILVER-compliant**: All six dimensions documented; SEC satisfied; SRI bounded
- [ ] **Partially compliant**: Some dimensions incomplete (list which)
- [ ] **Non-compliant**: Significant gaps (describe)

**Assessor Notes**:
> *(Final assessment and recommendations)*
