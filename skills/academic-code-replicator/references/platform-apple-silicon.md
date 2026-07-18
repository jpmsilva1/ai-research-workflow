### Apple Silicon (M1/M2/M3) Replication Traps

1. **Pre-2021 TensorFlow (TF < 2.4)**
   *Issue*: Will NOT compile or run natively on ARM64.
   *Adaptation Strategy*:
   - Option A: Install `tensorflow-macos` and `tensorflow-metal` (only works for TF 2.5+)
   - Option B: Force execution under Rosetta 2.
     Run `env /usr/bin/arch -x86_64 /bin/zsh` to open an x86 shell, then create a conda environment for x86:
     `CONDA_SUBDIR=osx-64 conda create -n x86_env python=3.7`
     `conda activate x86_env`
     `conda config --env --set subdir osx-64`
   - Option C (Recommended): Modify code (Phase 3) to use modern TF 2.13+, which supports Apple Silicon out of the box, handling deprecations.

2. **C-Compiler Missing / Homebrew Paths**
   *Issue*: ARM64 Homebrew installs to `/opt/homebrew`, while x86 used `/usr/local`. Old makefiles hardcode `/usr/local`.
   *Fix*: Modify Makefiles (Phase 3) to use `$(brew --prefix)` or manually patch paths to `/opt/homebrew`.

3. **Sleep Prevention**
   *Requirement*: MacBooks sleep aggressively, killing long runs.
   *Fix*: Wrap the execution script:
   ```bash
   caffeinate -i &
   CAFF_PID=$!
   python src/adapted/main.py
   kill $CAFF_PID
   ```
