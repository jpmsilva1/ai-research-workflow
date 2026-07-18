### R-Specific Replication Traps

1. **The `doParallel` Memory Bomb**
   R's `doParallel` default behavior on macOS/Windows creates a socket cluster. This copies the ENTIRE global environment into RAM for EVERY worker.
   If data = 5GB and cores = 16 → 80GB RAM used → instant OOM.
   *Fix*: Use FORK clusters on Linux/macOS (`makeCluster(cores, type="FORK")`), or better, use native package multithreading (e.g., `ranger(num.threads=cores)`) and set `doParallel` cores to 1.

2. **Package Archiving (CRAN)**
   CRAN aggressively removes packages that fail checks on new R versions.
   *Error*: `package 'X' is not available for this version of R`
   *Fix*: Install from the CRAN archive using `remotes`:
   ```R
   install.packages("remotes")
   remotes::install_version("PackageName", version="1.2.3")
   ```

3. **Tidyverse Breaking Changes**
   Code from 2017 using `dplyr` often breaks due to standard evaluation (`_()`) vs non-standard evaluation changes (NSE).
   *Fix*: Pin `dplyr` to a pre-1.0 version (e.g., `0.8.5`), or rewrite the specific failing `mutate`/`select` call using modern `{{ }}` syntax.

4. **Factor vs Character**
   R 4.0.0 changed `stringsAsFactors = FALSE` as the default.
   Pre-2020 code often assumes strings in dataframes are automatically factors, leading to modeling crashes.
   *Fix*: Add `options(stringsAsFactors = TRUE)` at the top of the main script.
