#!/bin/bash
# Phase 1 Ingestion: Automated Repo Audit Script
# Extracts entry points, hardcoded paths, and dependency signals.

TARGET_DIR=${1:-src/original/}

echo "=== Entry Points ==="
find "$TARGET_DIR" -type f \( -name "main.py" -o -name "train.py" -o -name "run_*.py" -o -name "*.R" -o -name "*.jl" \) -not -path "*/\.*"

echo -e "\n=== Hardcoded Paths (Potential Phase 3 Fixes) ==="
# Matches paths starting with / or Windows drives like C:\
grep -rnE "['\"](/[a-zA-Z]|[a-zA-Z]:\\\\)" "$TARGET_DIR" 2>/dev/null | grep -vE "(http|__)" | head -n 20

echo -e "\n=== Dependency Files ==="
find "$TARGET_DIR" -maxdepth 2 -type f \( -name "requirements.txt" -o -name "environment.yml" -o -name "renv.lock" -o -name "Project.toml" \)

echo -e "\n=== Detected Parallelism ==="
grep -rnE "(multiprocessing|joblib.Parallel|doParallel|mclapply|Threads.@threads)" "$TARGET_DIR" 2>/dev/null
