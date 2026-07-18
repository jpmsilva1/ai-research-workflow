### Julia-Specific Replication Traps

1. **Manifest.toml vs Project.toml**
   If the repo has both, `Pkg.instantiate()` will try to install the EXACT versions in `Manifest.toml`.
   If it's old (Julia 1.0 - 1.5), this often fails due to changed package URLs or system dependencies.
   *Fix*: If exact instantiation fails, delete `Manifest.toml` and run `Pkg.resolve()` to generate a new one based on `Project.toml` constraints.

2. **Julia Version Compatibility**
   Code written for Julia 0.6 will NOT run on Julia 1.x (massive syntax changes).
   Code written for Julia 1.x is generally forward-compatible, but package dependencies might not be.
   *Fix*: Use `juliaup` to install the specific minor version of Julia the paper used.

3. **Precompilation Hangs**
   Sometimes `using Package` hangs forever during precompilation on clusters.
   *Fix*: Run `Pkg.precompile()` explicitly in the environment setup phase.
