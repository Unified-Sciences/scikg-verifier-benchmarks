# SciKG Verify: scientific verification for physical and biological systems

## Method summary

SciKG Verify treats a model prediction as a scientific claim to be checked
against a temporally filtered evidence graph. For the P-glycoprotein benchmark,
the candidate claim is that a molecule has a particular probability of being
a P-glycoprotein inhibitor. A frozen molecular predictor supplies the initial
score. The verifier retrieves compatible pre-cutoff evidence, represents
supporting and conflicting relations, estimates evidence reliability and
applicability, and then decides whether the initial score should be retained or
corrected.

Evidence is admissible only when it predates the benchmark cutoff and passes
the method's entity, endpoint, directionality, and source-compatibility checks.
The held-out test labels, benchmark-derived target values, and post-cutoff
evidence are excluded from the graph and from verifier selection. Verifier
configuration is selected on validation data and frozen before the official
five-seed test evaluation.

## TDC evaluation contract

- benchmark group: `ADMET_Group`
- endpoint: `Pgp_Broccatelli`
- metric: ROC-AUC
- official seeds: 1, 2, 3, 4, 5
- official held-out rows: 245 per seed
- result: 0.9432418022 +/- 0.0018795697 ROC-AUC
- per-seed values: 0.9417488670, 0.9427486004, 0.9450813117,
  0.9412823247, 0.9453479072

Every final test prediction is included with a script that recomputes the
metric against the official TDC data. A versioned HTTPS service reproduces the
same predictions from the ordered candidate rows.

## Evaluation boundary

The verifier uses scientific evidence published before the benchmark cutoff.
It never receives held-out labels, benchmark-derived target values, or
post-cutoff evidence. The released predictions, row ordering, seeds and hashes
fully determine the reported metrics.
