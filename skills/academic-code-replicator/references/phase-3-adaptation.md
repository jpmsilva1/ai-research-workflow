### Purpose
Safely modify the experiment code so it runs in the current environment while strictly preserving its scientific behavior.

### The Sacred Boundary Rule in Practice
1. Never edit a file inside `src/original/`.
2. When a file needs modification, copy it to `src/adapted/` (keep the same relative path).
3. Edit the copy in `src/adapted/`.
4. Update the orchestration script (Phase 4) to run the adapted file instead of the original.

### Allowed vs. Forbidden Adaptations

**Allowed (Required for Execution)**:
- Fixing pathing issues (hardcoded absolute paths → relative paths)
- Changing how data is loaded (if format changed or it's too large for memory)
- Replacing deprecated library calls with modern equivalents
- Adding logging/progress bars to track long-running loops
- Fixing compilation/C-extension crashes (e.g., NumPy `np.float` → `float`)
- Adding argument parsing to make hardcoded hyperparameters configurable
- Adjusting parallelization/threading (e.g., removing `doParallel` socket clusters in R and replacing with native multithreading to avoid OOM)

**Forbidden (Changes Science)**:
- Changing model architecture, layer sizes, or activations
- Changing random seeds
- Changing optimizer types or learning rates
- Changing loss functions
- Changing the training loop logic (unless fixing a clear bug that prevents running)
- Altering evaluation metrics formulas

### Step-by-Step Adaptation Process

1. **Pathing Audit**:
   - Find all `read_csv`, `np.load`, `pd.read_`, `open()`, `load()`
   - Replace absolute paths (`/home/user/data/`) with relative paths (`../../data/`)
   - Prefer using `os.path.join` or `pathlib` in Python.

2. **Deprecation Fixes**:
   - Address Error Type C (from Phase 2).
   - If a function was moved: update the import.
   - If a function was removed: re-implement it minimally. (Example: `tfa.layers.WeightNormalization` → wrap a standard Dense layer).

3. **Data Handling (The OOM Risk)**:
   - Does the code load the entire dataset into RAM at once?
   - If dataset is > 10GB, this will OOM on standard machines.
   - Adaptation: Convert to generator/DataLoader if possible, OR explicitly document the RAM requirement for Phase 4 (cluster).

4. **Parallelism (The Silent Killer)**:
   - Identify `multiprocessing`, `joblib.Parallel`, R's `doParallel`/`mclapply`.
   - Watch out for R's `doParallel` socket clusters which duplicate the entire global environment. (See `lang-r.md` for the memory bomb breakdown and fix).
   - Adaptation: Change parallelization strategy to use native multithreading or drastically reduce cores.

5. **Configurability**:
   - If the original script has `EPOCHS = 100` hardcoded, adapt it to take an argument: `parser.add_argument('--epochs', default=100)`.
   - This allows Phase 4 to run smaller tests without editing code again.

### Code Modification Log
For every file modified, write an entry in REPLICATION_LOG.md:

```markdown
### Adaptation: {filename}
- **Copied to**: `src/adapted/{filename}`
- **Changes**:
  - Replaced hardcoded `/home/bob/data` with relative `../../data`
  - Replaced `tensorflow-addons` import with custom `WeightNorm` class
  - Exposed `batch_size` as CLI argument
- **Scientific Impact**: None.
```
