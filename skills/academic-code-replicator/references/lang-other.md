### Purpose
Fallback strategies for replicating experiments written in languages without dedicated reference documents (e.g., C++, MATLAB, Java, C#).

### 1. General Principles
- **Sacred Boundary Remains**: Always maintain `src/original/` and `src/adapted/`.
- **Containers as a Last Resort**: For compiled languages (C++/Java) with deep system dependencies, generating a `Dockerfile` matching the year of publication (e.g., `ubuntu:16.04`) is often faster than fixing local compilation errors.

### 2. C / C++
- **Issue**: Standard libraries change, GCC versions deprecate flags.
- **Adaptation**:
  - Edit the `Makefile` or `CMakeLists.txt` (in `src/adapted/`).
  - Add `-std=c++11` or `-std=c++14` if old code fails to compile with modern GCC.
  - Disable warnings treated as errors (`-Wno-error`).

### 3. MATLAB / Octave
- **Issue**: Requires a proprietary, expensive license.
- **Adaptation**: 
  - Check if the code is compatible with **GNU Octave** (open-source alternative). Write the orchestrator to call `octave run.m`.
  - Watch for proprietary toolboxes (e.g., Deep Learning Toolbox) which Octave lacks. If missing, document the failure clearly in `REPLICATION_LOG.md` — this is a valid replication roadblock.

### 4. Java / JVM Languages
- **Issue**: Heap space OutOfMemory (OOM) errors.
- **Adaptation**: If the code crashes with `java.lang.OutOfMemoryError`, adapt the orchestrator script to pass higher memory flags to the JVM: `java -Xmx16G -jar experiment.jar`.
