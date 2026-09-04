# SciKG Verify benchmark reproductions

This repository reproduces the benchmark results reported for SciKG Verify.
Each result includes the submitted predictions, immutable hashes, benchmark
metadata, and a small script that recomputes the score from end to end.

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

## MatBench dielectric

The `benchmarks/matbench_v0.1_SciKG_Verify` folder contains the native
MatBench recording for the five official `matbench_dielectric` folds:

- frozen MODNet v0.1.12 MAE: **0.2711019242**
- SciKG Verify MAE: **0.2493295679**
- relative MAE reduction: **8.0311%**
- paired reduction 95% interval: **0.0176199 to 0.0260036**
- one-sided paired sign-flip p-value: **0.0000500**

The native `results.json.gz` contains all 4,764 held-out predictions and is
accepted by MatBench's official submission validator. The accompanying client
requests the same version-pinned verifier output from the public serverless
endpoint. The complete evaluation
protocol is recorded in `info.json` and [METHOD.md](METHOD.md).

## Additional MatBench headline results

The `matbench_sota` bundle contains final held-out predictions and labels for
six additional five-fold evaluations:

- Log bulk modulus: **0.0476983337 MAE**
- Log shear modulus: **0.0647780857 MAE**
- Formation energy: **0.0168898491 MAE**
- Materials Project band gap: **0.1555109980 MAE**
- Perovskites: **0.0268923162 MAE**
- Glass formation: **0.9632361970 balanced accuracy**

Run `python matbench_sota/reproduce_metrics.py` to validate the immutable
prediction archive and recompute all 30 fold-level scores and six reported
means using only the Python standard library. The bundle exposes final outputs
and benchmark labels without distributing the private evidence graph or
verifier implementation.

The corresponding upstream submission is
[materialsproject/matbench#366](https://github.com/materialsproject/matbench/pull/366).
