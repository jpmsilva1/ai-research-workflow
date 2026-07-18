### Purpose
Execute the adapted code to generate results, managing runtime, hardware constraints, and potential crashes.

### Step 0: Sandboxing Recommendation
This phase executes arbitrary third-party code. Strongly recommend the user run this inside a Docker container, VM, or isolated environment. The Sacred Boundary protects the source code, but provides ZERO execution isolation on the host machine.

### Step 1: Write the Orchestrator
Never run a complex sequence of manual commands. Write an orchestration script in the root directory.
Prefer bash (`run_experiment.sh`) or a simple Python script (`run_all.py`).
(If `ponytail` skill is available, use it to ensure minimal complexity).

The orchestrator must:
1. Ensure the environment is active
2. Define paths explicitly (input data, output directories)
3. Run the adapted code, NOT the original code
4. Capture logs (stdout and stderr) to a file (e.g., `results/logs/run_YYYYMMDD_HHMMSS.log`)

**MANDATORY GATE**: Before executing the orchestrator script, you MUST present the script to the user and wait for explicit approval. Do NOT proceed to Step 2 until the user says "Yes, run it."

### Step 2: The Smoke Run
Before a full run, do a "smoke run" to ensure the pipeline connects end-to-end.
- Train for 1 epoch instead of 100
- Use 1% of the data
- Use 2 cross-validation folds instead of 10

If the smoke run crashes, go back to Phase 3.

### Step 3: Hardware & Runtime Assessment
Estimate full execution:
- Does it require a GPU? (CUDA out of memory?)
- Will it take > 12 hours?
- Will it require > 32GB RAM?

**Decision Matrix**:
1. Local execution feasible → Proceed to Step 4 (Local).
2. Requires cluster (SLURM) → Proceed to Step 4 (Cluster). (Trigger `distributed-gpu-engineer` bridge if available).

### Step 4 (Local): Execution & Sleep Prevention
For runs taking hours on a local machine, you must prevent sleep/suspend. 
If running on a local Mac, ensure the system doesn't sleep mid-training. (See `platform-apple-silicon.md` for `caffeinate` usage). On Linux, consider `systemd-inhibit`.

### Step 4 (Cluster): SLURM Execution
If local execution is impossible, create a SLURM batch script. Load `references/platform-cluster.md` for templates.
Write the script to `scripts/submit_job.sh`.

### Step 5: Monitoring
If running locally as a background task, use the `schedule` tool to check progress periodically (e.g., every 30 minutes). Do not busy-loop.

Check the logs for:
- Silent failures (NaN loss, converging to 0 immediately)
- Out of Memory (OOM) killer invocations (Linux `dmesg`, macOS `log show`)
- GPU memory fragmentation

### Completion Log Entry
```markdown
## {YYYY-MM-DD} Phase 4: Execution Complete
- **Duration**: {X} hours
- **Hardware**: {Local M2 Max / SLURM V100}
- **Logs saved to**: `results/logs/...`
- **Outputs generated**: {list main output files/tables}
```
