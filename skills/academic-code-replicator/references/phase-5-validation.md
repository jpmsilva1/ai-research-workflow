### Purpose
Compare the replication results to the original paper's reported results, apply scientific tolerance, and document deviations transparently.

### Step 1: Export Results
All results must be exported to CSV files in `results/tables/`.
If the experiment outputs custom formats (`.Rdata`, `.npz`, `.pkl`, `.pt`), write a short extraction script in `src/adapted/` to convert the final metrics into CSV.

### Step 2: Build Comparison Table
For each key metric from the paper, create this table in the experiment README.
The table must mirror the paper's own structure — use the same method names, same metric names, and same ordering the paper uses.

```markdown
## Key Results

| Method / Config     | Metric | Paper Value | Replicated Value | Δ (abs) | Δ (%)  | Status        | Note                          |
|---------------------|--------|-------------|-----------------|---------|--------|---------------|-------------------------------|
| LSTM (standard)     | RMSE   | 0.342       | 0.338           | −0.004  | −1.2%  | ✅ Match       | —                             |
| TCN (standard)      | RMSE   | 0.285       | 0.291           | +0.006  | +2.1%  | ✅ Match       | —                             |
| LSTM (weighted)     | SERA   | 12.4        | 14.1            | +1.7    | +13.7% | ⚠️ Deviation  | TF-addons re-impl.; see §Dev  |
| ST-Under (spatial)  | RMSE   | 0.198       | —               | —       | —      | ❌ Mismatch   | Crashed; C compiler missing   |
```

**Status legend** (three levels — use consistently across the entire table):
- `✅ Match` — difference is within tolerance for this method type (see Step 3)
- `⚠️ Deviation` — outside tolerance but cause is understood and documented; core finding still holds
- `❌ Mismatch` — cannot reproduce; cause unknown, or the experiment did not complete

**Column rules**:
- `Method / Config` — use the paper's exact label, including abbreviations the paper uses
- `Paper Value` — copy the exact number from the paper; do not round further
- `Replicated Value` — your result; write `—` if the run did not complete
- `Δ (abs)` — `Replicated − Paper`, with sign; write `—` if no replicated value
- `Δ (%)` — `(Replicated − Paper) / |Paper| × 100`; write `—` if Paper Value is 0 or missing
- `Status` — one of the three values above; never leave blank
- `Note` — brief free-text; write `—` if nothing to add

### Step 3: Apply Tolerance Guidelines
| Method type                            | Tolerance         | Mark as |
|----------------------------------------|-------------------|---------|
| Deterministic (same seed, same data)   | < 0.01% relative  | ✅ Match |
| Stochastic (averaged over ≥10 seeds)   | ≤ 5% relative     | ✅ Match |
| Different library versions             | ≤ 10% relative    | ✅ Match (document version diff in Note) |
| Different hardware (GPU vs CPU float)  | ≤ 2% relative     | ✅ Match |
| Outside tolerance, cause understood    | Any               | ⚠️ Deviation |
| Outside tolerance, cause unknown       | Any               | ❌ Mismatch |

### Step 4: Document Deviations
Any metric marked `⚠️ Deviation` or `❌ Mismatch` requires a detailed "Observations & Deviations" section below the table.

```markdown
## Observations & Deviations

### Deviation 1: SERA metric 13.7% above paper
- **Cause**: Paper used `tensorflow-addons 0.12` for WeightNormalization; we re-implemented it using standard Keras layers. Small numerical differences accumulate across 30 epochs.
- **Impact**: RMSE matches perfectly; SERA is slightly off. The paper's core finding (that LSTM outperforms TCN) still holds.
- **Classification**: Acceptable — caused by legitimate version incompatibility, not methodology failure.
```

### Step 5: Final Replication Log Entry
Append the final status to REPLICATION_LOG.md:
```markdown
## {YYYY-MM-DD} Phase 5: Validation Complete
**Overall Status**: [SUCCESS / PARTIAL / FAILED]
**Key Finding**: [One sentence summary of whether the paper's claims held up]
**Final comparison table generated at**: `{path_to_readme}`
```

Trigger **Bridge 4 (save-session)** to conclude the replication.
