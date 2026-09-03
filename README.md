# SciKG Verify benchmark reproductions

This repository reproduces the benchmark results reported for SciKG Verify.
Each result includes the submitted predictions, immutable hashes, benchmark
metadata, and a small script that recomputes the score from end to end.

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

The corresponding upstream submission is
[materialsproject/matbench#366](https://github.com/materialsproject/matbench/pull/366).
