# Core Pack Usage Guide (Academic Research)

This guide introduces the core toolset designed specifically for academic research, literature review, and Agent-Native Research Artifacts (ARA) compilation. By utilizing these tools, researchers can systematically decrease literature review times while increasing epistemic rigor.

## Invocation Patterns

Agent skills act as strict behavioral contracts. You can invoke them in two ways:
1. **Implicit Invocation (Default):** The agent automatically determines the necessary skill based on your natural language prompt.
2. **Explicit Invocation (Recommended):** Directly commanding the agent to assume a skill ensures maximum adherence to the framework.
   *Example: "Assume the `deep-research` skill and analyze the state of the art in graph neural networks."*

## Phase 0: Literature Review and Ideation

Before interacting with data, it is imperative to establish the state of the art. The Core Pack offers powerful search and synthesis tools:

- **`papers-skill`**: Directly interfaces with Semantic Scholar (200M+ papers) and arXiv. Use this to fetch references, verify citations, and extract PDF text autonomously.
- **`deep-research`**: An autonomous researcher. It continuously queries, reads, and synthesizes multiple web sources to construct comprehensive state-of-the-art reports.
- **`exa-search` & `tavily-web`**: Semantic search engines designed for LLMs. These tools extract complete tutorials and deep web content rather than just superficial metadata.
- **`brainstorming-research-ideas`**: A structured ideation framework designed to discover high-impact research directions and novel problem spaces.
- **`creative-thinking-for-research`**: Applies cognitive science frameworks (analogical reasoning, constraint manipulation) to force genuinely novel research directions.

## Phase 1: Agent-Native Research Artifacts (ARA)

To prevent LLM hallucination when reading complex PDFs, the workflow converts papers into highly structured data objects called Agent-Native Research Artifacts (ARA).

- **`ara-compiler`**: The core ingestion engine. It compiles raw PDFs, codebases, or notes into a structured ARA containing cognitive layers (claims, heuristics) and physical layers (configs, code stubs).
- **`ara-research-manager`**: The provenance tracker. Used exclusively at the end of a session as an epilogue. It scans conversation history to extract decisions, dead ends, and pivots, maintaining an auditable trace of the research evolution.
- **`ara-rigor-reviewer`**: Performs a Level 2 semantic epistemic review. It scores the ARA across six dimensions (evidence relevance, falsifiability, scope calibration, etc.) and issues a definitive Accept/Reject recommendation.

## Phase 2: Scientific Writing and Presentation

Once the methodology is validated and the data is gathered, these tools assist in generating publication-ready outputs.

- **`ml-paper-writing`**: Drafts highly rigorous ML/AI papers targeted at NeurIPS, ICML, ICLR, etc. It structures arguments and verifies citations for camera-ready submissions.
- **`academic-plotting`**: Generates publication-quality figures for ML papers. It autonomously selects the correct chart type (matplotlib/seaborn) based on experimental data or architectural descriptions.
- **`latex-paper-conversion`**: Automates the conversion of LaTeX academic papers between different journal formats (e.g., Springer, IPOL to MDPI, IEEE, Nature) by resolving formatting conflicts.
- **`2slides-ppt-generator`**: An AI-powered presentation engine. Summarizes Markdown documents, ARAs, or experiment logs into professional slide decks.
