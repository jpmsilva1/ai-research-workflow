---
name: academic-code-replicator
description: >
  Full-lifecycle skill for replicating experiments from academic papers. Guides
  the agent through understanding the original codebase, constructing isolated
  environments, making safe platform-compatibility adaptations, executing on
  available hardware, and producing a documented comparison against paper-reported
  results. Use this skill whenever the user says things like: "replicate this
  paper", "reproduce this experiment", "make this old code run", "run this
  paper's code", "I'm trying to get this GitHub repo from a paper working",
  "help me replicate these results", "this code is from 2019 and won't install",
  "I need to reproduce Table X from this paper", or any variation of scientific
  code replication. PROACTIVELY trigger even if the user just says "help me run
  this paper's experiments" without explicitly mentioning replication.
version: 1.1.0
tags: [replication, reproducibility, academic, research, experiments, dependencies, legacy-code]
---

## 1. The Core Principle

Academic code replication is an **archaeology problem**, not a software engineering problem. The fundamental tension that drives every decision in this skill is:
**You must not change what the experiment *computes*, but you often must change how it *runs*.**
This skill is grounded in real replication sessions: R code OOM-crashing at 78GB, TensorFlow 2.3 refusing to install on ARM64, nested loops taking 95 million iterations, C compilers silently missing. The protocols here are not theoretical best practices — they are patterns distilled from those failures.

## 2. When To Use / When NOT To Use

**Use when**: User is working with existing code from a published paper and wants to run it and verify results.
**Do NOT use when**: User wants to RE-IMPLEMENT a paper from scratch (different goal — recommend `ml-engineer` or domain skill). User has their own original codebase they want to debug (use standard debugging, not this skill). User wants to understand a paper theoretically without running code.

## 3. Phase Overview

| Phase | Name | Goal | Reference Doc |
|-------|------|------|---------------|
| 0 | Context Detection | Profile user's environment, route correctly | `references/context-detection.md` |
| 1 | Ingestion & Comprehension | Read-only code audit before touching anything | `references/phase-1-ingestion.md` |
| 2 | Environment Construction | Create isolated, working dependency environment | `references/phase-2-environment.md` |
| 3 | Code Adaptation | Safe modifications to make code run on this platform | `references/phase-3-adaptation.md` |
| 4 | Execution & Monitoring | Run safely on available hardware | `references/phase-4-execution.md` |
| 5 | Validation & Documentation | Compare results to paper; document everything | `references/phase-5-validation.md` |

## 4. Context Detection (Phase 0)

Execute this inline before loading any phase docs.

**Step 1 — Detect OS and architecture:**
Run or ask: What OS? (macOS/Linux/Windows). If macOS, is it Apple Silicon (M1/M2/M3) or Intel? This determines which platform doc to load.

**Step 2 — Detect knowledge source about the paper:**
Ask the user (or infer from context) which of these they have:
- (A) A compiled ARA or knowledge artifact in a knowledge base
- (B) The paper PDF locally
- (C) A URL/DOI to the paper
- (D) Only the code repository URL/path

Load accordingly: A → read ARA. B → read methodology + experiments sections. C → fetch abstract + code link. D → treat code as source of truth.

**Step 3 — Detect project structure:**
Check if user has an existing experiment directory with conventions. If yes, ask: "Do you have a specific folder structure or conventions I should follow?" If no structure exists → propose creating the Minimal Replication Package (MRP).

**Step 4 — Check for available skills (optional orchestration):**
Note which of these skills are available in the user's ecosystem (do not require any of them):
- `ara-compiler`: Can compile paper into structured knowledge artifact
- `distributed-gpu-engineer`: Can deploy long-running jobs to SLURM/HPC
- `ponytail`: Keeps orchestration scripts minimal (YAGNI)

After completing steps 1-4, write a brief **Environment Profile** to the session's replication log before proceeding.

**Environment Profile format** (write verbatim in log):
```
## Environment Profile
- **OS/Arch**: [macOS arm64 / macOS x86 / Linux x86 / Windows / Linux arm64]
- **Paper knowledge**: [ARA / PDF / URL only / Code only]
- **Project structure**: [Existing: {path} / MRP created at: {path}]
- **Available skills**: [list or "none detected"]
- **Platform doc**: [references/platform-{apple-silicon|linux|cluster|windows}.md]
- **Language doc**: [references/lang-{python|r|julia|other}.md]
```

## 5. The Minimal Replication Package (MRP)

When the user has no existing structure, create exactly this:

```
{experiment_name}/
├── REPLICATION_LOG.md    ← Create first. Template below.
├── src/
│   ├── original/         ← Original code goes here. NEVER MODIFIED.
│   └── adapted/          ← All your modifications go here.
└── results/
    ├── tables/
    └── figures/
```

REPLICATION_LOG.md initial content to write:
```markdown
# Replication Log: {paper_title}

**Paper**: {paper_title}
**Code source**: {repo_url}
**Replication started**: {YYYY-MM-DD}
**Target results**: [fill after reading paper]

---

<!-- Most recent entries at TOP -->

## {YYYY-MM-DD} Environment Profile
{paste the environment profile output from Context Detection}
```

## 6. The Sacred Boundary Principle

> **The Sacred Boundary Principle**: `src/original/` contains the authors' code, frozen at the moment of replication. It is NEVER modified. `src/adapted/` contains copies of files you need to change. Two years from now, the diff between these directories is your scientific audit trail — proof of exactly what you changed to make the code run, and what you did not touch.
>
> If the user's existing structure uses different directory names, respect those names. The principle is what matters: one directory frozen, one for adaptations.

## 7. Phase Execution Instructions

1. **Always run Phase 0** (Context Detection) inline — do not load a reference doc.
2. **Load the phase reference doc at the START of each phase**. Use it. Then proceed.
3. **Load the language doc** when the primary language is confirmed in Phase 1.
4. **Load the platform doc** once and keep it loaded for Phases 2–4.
5. **Do not skip phases**. Each phase produces output that the next phase depends on.
6. **Write to REPLICATION_LOG.md** at the end of every work session, not just at the end of the replication.

## 8. Skill Bridge Protocol

**Bridge 1 — ara-compiler** (trigger: after Context Detection, ONLY IF detected as available in Phase 0):
Say: "I can compile this paper into a structured knowledge artifact using the `ara-compiler` skill, which will give me richer context for the replication. Would you like to do that first? (recommended if you plan to replicate multiple papers or want persistent knowledge)"
If yes → hand off to ara-compiler with paper PDF/URL → receive ARA → use as Phase 1 input.
If no or skill absent → proceed with available knowledge.

**Bridge 2 — ponytail** (trigger: during Phase 4, when writing orchestration scripts):
When creating orchestration scripts (run_all.sh, run_parallel.py, evaluate.py), prefer minimal implementations. If `ponytail` skill is available, invoke it for script creation. If not, apply the principle manually: shortest code that correctly orchestrates the experiment. No speculative abstractions.

**Bridge 3 — distributed-gpu-engineer** (trigger: Phase 4, when runtime > 12 hours):
Say: "This experiment's estimated runtime exceeds 12 hours on local hardware. I recommend deploying it to a compute cluster. [If skill available:] I can hand this off to the `distributed-gpu-engineer` skill to set up the SLURM job. [If not:] I'll document the cluster requirements and provide a SLURM template from the platform-cluster reference."
Handoff context to provide: experiment directory path, the exact run command, estimated RAM, estimated runtime, language/framework.

**Bridge 4 — save-session / Obsidian** (trigger: end of Phase 5, ONLY IF detected as available in Phase 0):
Say: "Replication complete. Would you like to file the key findings (what worked, what needed adaptation, any deviations) to your knowledge base for future reference?"
If Obsidian/save-session available → write structured log entry with links.
If not → ensure REPLICATION_LOG.md is comprehensive enough to serve as the permanent record.
