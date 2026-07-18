### Purpose
Create an isolated environment where the original code's dependencies are satisfied. Never install into the system runtime.

### Universal Rule
**One isolated environment per experiment.** venv, conda env, or renv — never system Python/R/Julia.

### Step 0: Dependency Supply-Chain Vetting
Before executing `pip install`, `conda env create`, or `renv::restore`, you MUST scan the manifest (`requirements.txt`, `environment.yml`) for suspicious packages. Academic repos are unvetted.
- Check for typosquatted packages (e.g., `tensroflow` instead of `tensorflow`).
- Look out for custom `setup.py` files downloading weird binaries.
- If you see anything suspicious, **STOP** and ask the user for permission.

### Step 1: Choose Isolation Tool
```
Language + manifest type → isolation tool:
├── Python + requirements.txt → python -m venv .venv  [OR]  conda create -n {name}
├── Python + environment.yml → conda env create -f environment.yml
├── Python + pyproject.toml → python -m venv .venv + pip install -e .
├── R + renv.lock → renv::restore()
├── R + no renv → conda create -n {name} r-base={version} + R install.packages()
├── Julia → julia --project=. -e "using Pkg; Pkg.instantiate()"
└── Mixed Python+R → conda (can manage both)
```

### Step 2: Python Version Estimation
If the paper's requirements.txt doesn't specify a Python version, estimate from publication year:

| Publication Year | Likely Python Version | Install as |
|-----------------|----------------------|------------|
| 2015–2017 | Python 3.5–3.6 | `python3.6` via deadsnakes PPA (Linux) or pyenv |
| 2018–2019 | Python 3.6–3.7 | `python3.7` |
| 2020–2021 | Python 3.7–3.8 | `python3.8` |
| 2022 | Python 3.8–3.9 | `python3.9` |
| 2023–2024 | Python 3.9–3.11 | `python3.10` |

Always document which Python version was used vs. what the paper likely assumed.

### Step 3: R Version Estimation
| Publication Year | Likely R Version |
|-----------------|-----------------|
| 2015–2017 | R 3.2–3.4 |
| 2018–2019 | R 3.5–3.6 |
| 2020–2021 | R 4.0 |
| 2022–2024 | R 4.1–4.3 |

### Step 4: Installation Attempt and Failure Classification

Attempt installation. If it fails, classify the error using this full taxonomy:

#### Error Type A: Version Not Found
```
Error: Could not find a version that satisfies the requirement tensorflow==2.3.0
```
**Strategy**: Find the nearest available version.
```bash
pip index versions tensorflow  # list all available
pip install tensorflow==2.13.0  # or nearest compatible
```
Always document the version change in REPLICATION_LOG.md.

#### Error Type B: Compilation Failure
```
Error: Failed building wheel for {package}
CMakeError / gcc: error / clang: error
```
**Strategy**: Depends on platform. Load `references/platform-{platform}.md` for exact commands.
General approach:
1. Try `conda install -c conda-forge {package}` (pre-compiled wheels)
2. If R package: check if C compilers are in the conda env (not just system)
3. If still fails: check if there is a pure-Python fallback or a newer version without C deps

#### Error Type C: Package Deprecated or Removed
```
ERROR: Could not find a version that satisfies the requirement tensorflow-addons
No matching distribution found for sklearn.externals
```
This is the most dangerous error type. The package no longer exists.
**Strategy**:
1. Identify which specific classes/functions from the package the code uses (grep the codebase)
2. Check if the functionality has been moved into the main package (e.g., `tensorflow-addons.WeightNormalization` → re-implement using TF base)
3. If not: plan a re-implementation. Do NOT resolve this in Phase 2 — flag it and handle in Phase 3.
4. Document: "Package X is deprecated. Code uses: [list functions]. Re-implementation planned for Phase 3."

Known deprecated packages lookup:
| Package | Status | Modern Alternative |
|---------|--------|--------------------|
| `tensorflow-addons` | Deprecated 2024 | Implement directly in TF or use keras |
| `sklearn.externals` | Removed in sklearn 0.23 | Install `joblib` directly |
| `torch.utils.data.dataloader` (old API) | Changed API | Use current API |
| `keras` (standalone, pre-TF2) | Merged into TF | `from tensorflow import keras` |
| `fastai v1` | Replaced by fastai v2 | Use v2 API or pin v1 |

#### Error Type D: Package Renamed
```
No module named 'sklearn'  →  scikit-learn
No module named 'cv2'  →  opencv-python
No module named 'PIL'  →  Pillow
```
Simply install the correct modern package name. Document.

#### Error Type E: Dependency Conflict
```
ERROR: pip's dependency resolver... package A requires X>=2.0, package B requires X<2.0
```
**Strategy**:
1. Try `conda` — it has a stronger solver than pip
2. Try `pip install --use-deprecated=legacy-resolver` as a fallback
3. If conflict is between the target package and a utility (e.g., numpy): check if a newer version of the target resolves it
4. As last resort: create two separate environments (one for training, one for evaluation)

#### Error Type F: No Manifest At All
If no `requirements.txt`, `environment.yml`, or similar exists:
1. Run `grep -r "^import\|^from" src/original/ --include="*.py" | sed 's/.*import //;s/ as.*//' | sort -u` to get import list
2. Separate stdlib imports (no install needed) from third-party
3. Build a requirements.txt manually: `{package}=={latest_stable}` for each
4. **MANDATORY GATE**: Present the generated `requirements.txt` to the user and wait for their explicit approval before running `pip install` (hallucinating a package name could pull malware).
5. Install, run smoke test, iterate on failures

### Step 5: Smoke Test
After environment setup, run the smallest possible test:
```bash
python -c "import {main_package_1}; import {main_package_2}; print('imports OK')"
```
Or for R: `source("main_script.R")` with a tiny subset of data.
If this fails → back to failure classification. Do not proceed to Phase 3 until imports are clean.
