# SciKG Verify benchmark reproductions

This repository reproduces the benchmark results reported for SciKG Verify.
Each result includes the submitted predictions, immutable hashes, benchmark
metadata, and a small script that recomputes the score from end to end.

## MatBench dielectric: completed five-fold evaluation

SciKG Verify reduces MODNet's prediction error on all five official folds of
MatBench dielectric. The September 6 release includes both evaluated variants:

| Model | MAE | Reduction versus MODNet |
| --- | ---: | ---: |
| MODNet v0.1.12 | 0.271102 | — |
| SciKG Verify | **0.251180** | **7.35%** |
| SciKG Residual | **0.247287** | **8.78%** |

Both results cover all 4,764 rows. Each outer test fold is excluded from the
feature selection, model selection and training that produce its correction
model's inputs. Ten fold-pair-excluded MODNet fits supply those inputs; the
official outer-fold base predictions and the original evidence snapshot and
correction rules are unchanged. The two variants are reported separately,
not combined by choosing whichever works best on each test fold.

This replaces the earlier selector archive (0.249330 MAE). The completed
evaluation retains 91.5% of its absolute error reduction. The versioned API
evaluates the fitted correction models on each request; it does not look up
stored final predictions. See [METHOD.md](METHOD.md) for the protocol and
[EVALUATION_STATUS.json](EVALUATION_STATUS.json) for the status of other tasks.

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

## Reproduce the dielectric results

The `benchmarks/matbench_v0.1_SciKG_Verify` and
`benchmarks/matbench_v0.1_SciKG_Residual` folders each contain a native
MatBench recording, reference labels and base predictions, statistics,
checksums, and an inference client.

From either folder:

```sh
python submission_client.py
python submission_client.py --live
python submission_client.py --live --record reproduced.json.gz
```

The first command checks the artifacts and recomputes all fold scores offline.
The second evaluates every candidate through the versioned API and checks the
returned predictions against the archive. The third records those live outputs
using MatBench 0.6 (an additional dependency). Requests contain candidate IDs,
fold and variant, never labels. The service holds the fitted models and
benchmark inputs; full retraining requires those service-side assets.

Paired bootstrap 95% intervals for the MAE reduction are **0.016048–0.023866**
for SciKG Verify and **0.020165–0.027480** for SciKG Residual. These intervals
resample rows within the five fixed folds and are conditional on the fitted
predictions; they do not estimate variation from retraining.

## Additional historical MatBench measurements

The `matbench_sota` bundle contains final held-out predictions and labels for
seven additional five-fold evaluations:

This older bundle is unchanged. Formation energy, Materials Project band gap,
perovskites and glass still need their upstream training dependencies resolved;
the dielectric evaluation does not resolve those tasks. Their listed values
are historical measurements, not confirmed leaderboard claims. The old
elastic-modulus corrections are superseded by completed outer-training-only
interval results: **0.064796 log shear MAE** and **0.048104 log bulk MAE**.
Those replacement bundles are not yet included here. Experimental band gap
uses a separate prediction pipeline, and the TDC results above are unchanged.
The older readiness file records bundle completion, not current claim status.

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
