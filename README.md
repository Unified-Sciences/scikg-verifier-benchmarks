# SciKG Verify benchmark reproductions

This repository reproduces the benchmark results reported for SciKG Verify.
Each result includes the submitted predictions, immutable hashes, benchmark
metadata, and a small script that recomputes the score from end to end.

## September 5 evaluation correction

**Five historical materials claims are deferred:** dielectric, formation
energy, Materials Project band gap, perovskites and glass. The old correction
models trained on other folds' out-of-fold base predictions. Under the official
base-model training contract, those predictions can depend on labels in the
eventual correction-model test fold. Excluding that fold's rows from the
correction model did not establish end-to-end exclusion of test information.

The old elastic-modulus corrections share that issue and are superseded by a
new method that never fits or calibrates on base predictions. Its primary MAEs
are **0.064796 for log shear modulus** and **0.048104 for log bulk modulus**;
the corresponding replacement prediction bundles are not yet included here.
The experimental band-gap pipeline is a separate result. This finding does
not establish a defect in the TDC evaluations.

Original prediction archives remain unchanged so the historical scores can
still be inspected. A passing numerical reproduction or submission-format
check is **not** validation of the training protocol. Do not use the affected
historical materials scores as confirmed leaderboard claims. See
[EVALUATION_STATUS.json](EVALUATION_STATUS.json) for machine-readable status.

Run `python verify_release.py` from the repository root to verify the immutable
artifacts and reproduce the published scores. The same command runs in CI on
every push and pull request.

## Additional TDC headline results

The `tdc_sota` bundle contains final held-out predictions and labels for four
additional five-seed ADMET evaluations:

- Ames mutagenicity: **0.8735406998 ROC-AUC**
- Drug half-life: **0.5860994384 Spearman correlation**
- Human intestinal absorption: **0.9950205761 ROC-AUC**
- AqSolDB solubility: **0.7126511346 MAE**

Run `python tdc_sota/reproduce_metrics.py` to validate the immutable prediction
archive, preserve every held-out row identity and order, and recompute all 20
seed-level scores and the four reported means using only the Python standard
library. The bundle contains final outputs and benchmark labels; it does not
contain the private evidence graph or verifier implementation.

## TDC P-glycoprotein

The `tdc_pgp` folder records the five official TDC seeds for
`ADMET_Group/Pgp_Broccatelli`:

- ROC-AUC: **0.9432418022 +/- 0.0018795697** (sample standard deviation)
- seeds: `1, 2, 3, 4, 5`
- test rows: `245` per seed
- prediction archive SHA-256:
  `0caa286f8c7478f5e5acb5464481aac226b0e20dec402176bc63eca95cfcb6a9`

Run `python tdc_pgp/reproduce_metrics.py` to verify the immutable prediction
and official-label snapshots, match every row identity, recompute all five
ROC-AUC values, and check the reported mean and standard deviation. The script
uses only the Python standard library and does not depend on a working PyTDC
installation or network service.

`tdc_pgp/submission_client.py` can also request the frozen predictions from the
versioned verifier endpoint. It defaults to `https://unified-sciences.com` and
does not require a credential because these submitted predictions are already
public. Set `SCIENTIA_VERIFIER_API_URL` only to test another compatible host.

See [METHOD.md](METHOD.md) for the method and evaluation protocol.

## Historical MatBench dielectric result — confirmation pending

The `benchmarks/matbench_v0.1_SciKG_Verify` folder contains the native
MatBench recording for the five official `matbench_dielectric` folds:

- frozen MODNet v0.1.12 MAE: **0.2711019242**
- SciKG Verify MAE: **0.2493295679**
- relative MAE reduction: **8.0311%**
- paired reduction 95% interval: **0.0176199 to 0.0260036**
- one-sided paired sign-flip p-value: **0.0000500**

The native `results.json.gz` contains all 4,764 held-out predictions and is
accepted by MatBench's submission-format validator, which does not validate
the upstream training boundary. The accompanying client
requests the same version-pinned verifier output from the public serverless
endpoint. The complete evaluation
protocol is recorded in `info.json` and [METHOD.md](METHOD.md).

## Additional historical MatBench measurements

The `matbench_sota` bundle contains final held-out predictions and labels for
seven additional five-fold evaluations:

The qualifications above apply to this preserved bundle; its old readiness
file records prediction-bundle completion, not current eligibility for a
scientific or leaderboard claim.

- Log bulk modulus: **0.0476983337 MAE**
- Log shear modulus: **0.0647780857 MAE**
- Formation energy: **0.0168898491 MAE**
- Materials Project band gap: **0.1555109980 MAE**
- Perovskites: **0.0268923162 MAE**
- Glass formation: **0.9632361970 balanced accuracy**
- Experimental band gap: **0.2855009001 MAE**

Run `python matbench_sota/reproduce_metrics.py` to validate the immutable
prediction archive and recompute all 35 fold-level scores and seven reported
means using only the Python standard library. The bundle exposes final outputs
and benchmark labels without distributing the private evidence graph or
verifier implementation.

The corresponding upstream submission is
[materialsproject/matbench#366](https://github.com/materialsproject/matbench/pull/366).
