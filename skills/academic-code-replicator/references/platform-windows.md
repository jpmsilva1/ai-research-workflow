### Purpose
Detailed environment adaptations required when executing legacy machine learning experiments on Microsoft Windows (or WSL2).

### 1. The Path Separator Problem
Windows uses `\` instead of `/` for paths. Legacy code often assumes POSIX paths.
- **Python**: If code uses `path = dir + "/" + file`, it might fail. Use `os.path.join()` or `pathlib`.
- **Hardcoded Drives**: Watch out for hardcoded `C:\\Users\\` or `D:\\datasets\\`. They must be changed to relative paths `../../data/`.

### 2. WSL2 Boundary Penalty
If running inside Windows Subsystem for Linux (WSL2), accessing files on the mounted Windows drives (`/mnt/c/`) incurs a massive I/O penalty (up to 100x slower).
- **Adaptation**: Move the entire dataset and codebase into the native Linux filesystem (`~/.` or `/home/user/`) inside WSL2 before running data-heavy experiments.

### 3. Native Compilation Issues (C++)
- Many older pip packages assume `gcc` or `make` are available. Windows lacks these natively.
- **Adaptation**: If a pip install fails due to missing C++ Build Tools, prefer using `conda install` instead of `pip`. Conda provides pre-compiled binaries for Windows.

### 4. Multiprocessing on Windows
- Windows does not support `os.fork()`. `multiprocessing` on Windows uses `spawn()`, which requires the entry point to be protected by `if __name__ == '__main__':`.
- **Note**: This is a Windows native problem. Inside WSL2, `fork()` works normally.
- **Adaptation**: If the script crashes with a RuntimeError about "freeze_support", wrap the main execution code inside the `__main__` block.
