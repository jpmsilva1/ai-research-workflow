### Linux (Ubuntu/Debian) Replication Traps

1. **Missing System Libraries**
   *Issue*: `pip install` fails on packages like `psycopg2`, `cv2`, `lxml` due to missing C headers.
   *Fix*: Search for the missing library via `apt-cache search` or just try to use `conda` which bundles these C libraries:
   `conda install -c conda-forge opencv`

2. **Out Of Memory (OOM) Killer**
   *Issue*: Script dies instantly with `Killed` printed to terminal. No Python traceback.
   *Diagnosis*: Run `dmesg -T | tail -n 20 | grep -i oom` or `grep -i oom /var/log/syslog`. If found, the OS killed the process for using too much RAM.
   *Fix*: Go to Phase 3. Reduce batch size, switch to iterators, or reduce parallel workers. If already minimal, escalate to Cluster (Phase 4).

3. **Sleep/Suspend Prevention**
   *Requirement*: If running on a local Linux workstation, prevent sleep.
   *Fix*: Wrap the execution script:
   ```bash
   systemd-inhibit --what=sleep:idle --who="experiment" --why="running replication" python src/adapted/main.py
   ```
