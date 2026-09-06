# SciKG Verify: scientific verification for physical and biological systems

## Completed dielectric evaluation — September 6, 2026

The benchmark is `matbench_dielectric`: 4,764 crystals, five official folds,
and mean absolute error in refractive index. The reference predictions are
the published MODNet v0.1.12 outputs (mean fold MAE 0.2711019242).

For each pair of official folds (a, b), MODNet is trained on the other three
folds and predicts both excluded folds. All feature selection, scaling,
architecture selection and fitting exclude a and b. Ten unordered pairs
therefore supply the twenty prediction vectors needed to train the outer-fold
correction models. For outer fold a, every correction-training prediction
comes from a model that excluded a as well as the row's own fold. The official
base predictions on outer fold a are unchanged.

These pair models use MODNet 0.1.12 and the modnet-matbench v0.4.0 recipe:
the complete featurizer, training-only feature selection, the full preset
search with five internal folds and five bootstrap networks, and the final
125-network ensemble. Models, selected features, row memberships and checksums
are archived privately. This is regenerated training, not recovery of the
unavailable historical base weights.

The original v2 evidence snapshot, evidence cutoff, direct correction,
nonlinear residual model and selector rules remain unchanged. This comparison
does not incorporate the later structure-confirmed evidence snapshot. It
repairs the outer-test training dependency while preserving the historical
internal selector procedure; it does not claim that every internal validation
layer of that procedure has become independently nested.

Two pre-existing variants are reported on every fold: SciKG Verify uses the
original selector, and SciKG Residual uses the nonlinear correction. Their
MAEs are 0.2511801222 and 0.2472874776, respectively. Both improve all five
folds. Neither result mixes variants based on held-out scores.

## Reproduction

Each release contains the native MatBench predictions, official reference
labels and base predictions, per-fold scores, paired bootstrap statistics,
and a manifest of file hashes. Offline reproduction recomputes the scores.
Live reproduction sends candidate IDs to a versioned service that evaluates
the fitted correction model using stored benchmark inputs. The API receives
no target labels and does not retrieve final predictions from a lookup table.
The client can record the returned predictions through the MatBench API.

The public driver reproduces inference and scoring, not full model training.
The evidence assets and fitted models remain on the service; independent
retraining requires access to those assets. The service contract is scoped
to the benchmark candidate IDs and is not a general new-crystal prediction API.

The bootstrap intervals resample rows within each fixed fold (20,000 draws,
seed 20260906). They quantify paired uncertainty conditional on the fitted
predictions, not training-seed variation.

## Other materials results

The older globally out-of-fold training inputs for formation energy, MP band
gap, perovskites and glass have not yet received the same regeneration.
The two elastic-modulus results instead have a completed replacement method
that fits source-context transfer on outer-training measurements, calibrates
on separate source groups, and never uses base predictions during fitting
or calibration. Their new bundles are pending. See `EVALUATION_STATUS.json`;
the completed MODNet dielectric evaluation does not change another task's
status. The TDC contract below is a separate evaluation.

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

## TDC evaluation boundary

The verifier uses scientific evidence published before the benchmark cutoff.
It never receives held-out labels, benchmark-derived target values, or
post-cutoff evidence. The released predictions, row ordering, seeds and hashes
fully determine the reported metrics.
