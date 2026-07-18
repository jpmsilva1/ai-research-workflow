### Purpose
Use these structured prompts to test the `academic-code-replicator` skill using the `/skill-creator` or any standard agent session. They simulate real-world legacy code replication scenarios to verify the skill triggers the correct bridges and adaptations.

---

### Test Case 1: The Apple Silicon Native Compilation Wall
**Simulates:** A 2020 Python project relying on an old version of TensorFlow that cannot be installed natively on an M-series Mac.
**Expected Agent Behavior:** Identifies OS as `arm64`, detects TensorFlow 2.3 in `requirements.txt`, triggers Phase 2 Error Type A (Version Not Found), and recommends Conda environment with macOS specific tensorflow-macos or Rosetta 2.

**Prompt to Agent:**
> "I need to replicate this paper. The code is in a folder `src/` and has a `requirements.txt` pinning `tensorflow==2.3.0` and `numpy==1.18.5`. I'm running on an M2 Mac. Please ingest and construct the environment."

---

### Test Case 2: The R Memory Bomb
**Simulates:** An R script using `doParallel` that will crash modern machines by duplicating the global environment across 16 cores.
**Expected Agent Behavior:** Phase 1 `audit_repo.sh` detects `doParallel`. Phase 3 flags it as a high-risk memory bomb (referencing `lang-r.md`) and proposes rewriting the loop to use native multithreading or drastically reducing `cores`.

**Prompt to Agent:**
> "Help me run this R experiment. The entry point is `run_simulations.R`. Inside, it loads a 5GB CSV file into a dataframe, then calls `makeCluster(16)` and `registerDoParallel()`, followed by a `foreach` loop over 1000 iterations. Fix it so it runs without crashing my laptop."

---

### Test Case 3: The Cluster Escalation (Bridge 3)
**Simulates:** A massively intensive deep learning script that exceeds local hardware capabilities.
**Expected Agent Behavior:** Phase 4 estimates runtime > 12 hours or requires massive VRAM. The agent triggers **Bridge 3** (`distributed-gpu-engineer`), pivoting from a local `bash` orchestrator to writing a SLURM `sbatch` script.

**Prompt to Agent:**
> "I want to reproduce the main training loop in `train_gpt2_reproduction.py`. The paper says it trained for 7 days on 8x V100 GPUs. I only have a local MacBook Pro, but I have SSH access to our university SLURM cluster. Proceed through Phase 4."
