### Cluster (SLURM) Replication Guide

Use this when `distributed-gpu-engineer` is not available, but the user needs to run the code on a cluster.

1. **Environment Export**
   You cannot run `pip install` on a compute node easily without internet.
   *Rule*: Build the conda/venv environment on the login node FIRST (Phase 2), then the compute node just activates it.

2. **SLURM Job Template & Blast Radius Warning**
   *Warning*: Executing unvetted code on a shared SLURM cluster using the user's SSH credentials has a massive blast radius. You MUST mandate user confirmation before submitting any jobs via `sbatch`.
   Provide this template to the user or write it to `scripts/submit_job.sh`:

   ```bash
   #!/bin/bash
   #SBATCH --job-name=replicate_experiment
   #SBATCH --output=results/logs/slurm_%j.out
   #SBATCH --error=results/logs/slurm_%j.err
   #SBATCH --partition=gpu            # Change to user's partition
   #SBATCH --gres=gpu:1               # Request 1 GPU
   #SBATCH --cpus-per-task=8          # Match your script's n_jobs
   #SBATCH --mem=64G                  # Prevent OOM
   #SBATCH --time=24:00:00            # Max walltime

   # 1. Load modules (if required by cluster)
   # module load miniconda3
   # module load cuda/11.8

   # 2. Activate environment
   source ~/.bashrc
   conda activate experiment_env

   # 3. Go to working directory
   cd /path/to/experiment/root

   # 4. Run the adapted code
   echo "Starting run at $(date)"
   python src/adapted/main.py --batch_size=32 --workers=8
   echo "Finished run at $(date)"
   ```

3. **Data Localization**
   *Issue*: Reading 100,000 small images directly from a shared network drive (NFS/Lustre) will freeze the cluster filesystem.
   *Adaptation*: Add code to the top of `submit_job.sh` to copy the dataset to the node's local scratch space (`$TMPDIR` or `/scratch/$USER`), and point the Python script there.
