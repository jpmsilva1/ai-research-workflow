### Purpose
Read-only comprehension of the codebase. The goal is to understand the experiment completely before touching anything. Every action in this phase produces knowledge, not changes.

### Step 1: Activate Prior Knowledge
```
Knowledge source routing:
├── ARA available → read it. Extract: claims, experimental setup, datasets, metrics, known issues, entry points.
├── Paper PDF → read Experiments section. Extract: datasets used, hyperparameters, number of runs/seeds, target metrics and values.
├── URL only → fetch README and abstract. Ask user: "What specific table or figure are we trying to reproduce, and what numbers does the paper report?"
└── Code only → proceed to Step 2. Treat code as the specification.
```

After this step, write one sentence in REPLICATION_LOG.md: "**Target**: Reproduce [Table X / Figure Y] from [paper title], specifically: [list the exact numbers from the paper you are trying to match]."

### Step 2: Repository Structure Map
First, execute `scripts/audit_repo.sh <target_dir>` to automatically identify entry points, hardcoded paths, and parallelism signals.

Then, manually list all files and group by type. Identify:

**Entry Points** (look for these specifically):
- Python: files containing `if __name__ == "__main__"`, files named `main.py`, `run_*.py`, `experiment.py`, `train.py`
- R: `.R` files in the root or `inst/` that use `source()` to load others; `run_*.R` files
- Julia: `run_*.jl`, `experiment.jl`, any script in root
- Any language: `Makefile`, `run.sh`, `experiments.sh`, `run_all.sh`
- Jupyter: `*.ipynb` notebooks (note: harder to parameterize, may need conversion)

**Configuration** (look for):
- `config.yaml`, `config.json`, `params.yaml` — likely contains hyperparameters
- Hardcoded constants at the top of main scripts
- `argparse` / `optparse` / `docopt` usage (good — configurable)
- No argument parsing at all (bad — will need adaptation)

**Data**:
- Where does the code expect data? (hardcoded path? `data/` relative? absolute?)
- Is the data included in the repo or downloaded separately?
- If downloaded: is there a download script? **SECURITY RULE**: You MUST flag any `wget`/`curl`/download scripts that do not point to trusted academic domains (e.g., HuggingFace, Zenodo, PhysioNet) with `❌ UNTRUSTED DOWNLOAD` and wait for explicit human approval before downloading.

### Step 3: Execution Graph
Starting from each entry point, trace the call chain. Write it out:
```
{entry_point}
  → imports/sources {file_A} → imports {file_B}
  → reads {data_file} [path: {actual path in code}] [hardcoded? yes/no]
  → writes {output_file} [path: {actual path}] [directory created automatically? yes/no]
```

**Red flags to flag explicitly in the log**:
- `❌ HARDCODED PATH`: Any absolute path (e.g., `/home/author/datasets/`, `C:\Users\...`)
- `❌ HARDCODED DATASET`: Dataset name as a variable set at the top of the script
- `❌ MISSING OUTPUT DIR`: Code writes to a directory without creating it first
- `❌ NESTED LOOPS ON LARGE DATA`: O(N²) or O(N×M) loops iterating over rows/samples
- `❌ MEMORY ACCUMULATION`: Results or data appended to a list inside a loop over many folds/iterations
- `❌ UNCONFIGURABLE PARALLELISM`: `n_jobs=8` hardcoded — will use all cores and may thrash

### Step 4: Dependency Pre-Audit
Read: `requirements.txt`, `environment.yml`, `renv.lock`, `setup.py`/`pyproject.toml`, or `DESCRIPTION` (R).

For each dependency, flag:
- `⚠️ PINNED OLD VERSION`: Version number is pinned and >2 years old
- `❌ KNOWN DEPRECATED`: Package is known to be deprecated or removed (see lang-specific reference docs for lookup table)
- `⚠️ COMPILATION LIKELY`: Package is known to require native compilation (check platform reference doc)
- `✅ STABLE`: Package appears stable and well-maintained

If no dependency file exists at all: `❌ NO MANIFEST — must infer from imports.`

### Step 5: Code Audit Log Entry
At the end of Phase 1, write this structured entry to REPLICATION_LOG.md:
```markdown
## {YYYY-MM-DD} Phase 1: Code Audit

### Entry Points
- {file}: {description}

### Execution Graph
{paste the execution graph}

### Red Flags
{list all ❌ flags found, or "None found"}

### Dependency Pre-Audit
{list each dep with status flag}

### Target Results
{exact numbers from paper we are trying to reproduce}

### Primary Language Detected
{Python / R / Julia / other}
→ Loading: references/lang-{language}.md
```

After writing this entry, load `references/lang-{detected_language}.md` before proceeding to Phase 2.
