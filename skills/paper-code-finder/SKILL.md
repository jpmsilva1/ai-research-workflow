---
name: paper-code-finder
description: Find source code implementations and GitHub repositories for academic AI/ML research papers. Use this skill whenever a user asks for the code, repository, huggingface, or implementation of a paper. Ensure you trigger this even if they just say "is there code for this?" while looking at a paper.
---

# Paper-Code-Finder: Code Discovery for Academic Papers

This skill locates the official or unofficial source code implementations for academic papers, utilizing highly efficient search strategies specifically optimized for the AI/ML ecosystem.

## 1. Input Processing & Entity Extraction
First, analyze the user's input to extract key metadata:
- **Title, Authors, Affiliations**: Extract these from the prompt, PDF, arXiv link, or DOI.
- **ML Framework Semantic Extraction**: If a PDF or abstract is provided, scan the "Experiments" or "Implementation Details" section for keywords like `PyTorch`, `JAX`, `Flax`, `TensorFlow`, or `Diffusers`. Use this to narrow down your search queries.

## 2. Search Strategy (The Waterfall)
Execute a structured, sequential search to find the code. Progress through these steps sequentially until you find a match. **For highest precision, explicitly use the `exa-search` or `tavily-web` skills/tools if they are available to you**.

### Phase 1: The Fast-Path (PapersWithCode)
1. Search `"[Title] paperswithcode"`. This is the most reliable database.

### Phase 2: The Hugging Face & Mega-Repo Hunter
1. Search `"[Title] site:huggingface.co/papers"` and `"[Title] site:huggingface.co"`.
2. If the paper is about foundational models, search for pull requests in mega-repos: `"[Title] huggingface/transformers github"` or `"[Title] huggingface/diffusers github"`.

### Phase 3: The Deep-Path (Author Profile Hunting)
If the above fail, the repo likely has an obscure name.
1. **Direct GitHub**: Search `"[Title] [Framework] site:github.com"`.
2. **Find the Authors**: Identify the First Author and the Last Author (Principal Investigator).
3. **Find their GitHub**: Search `"[Author Name] [University/Affiliation] site:github.com"`.
4. **Inspect the Profile**: Look at their pinned repositories or search within their GitHub profile for repos created around the paper's publication year.
5. **Personal Websites**: Search for the author's academic homepage (e.g., `"[Author Name] [University] homepage"`).

## 3. Verification & Classification
When repositories are found, evaluate them:
- **Official Implementation**: Owned by the paper's authors, or explicitly linked inside the paper text/author's website/PapersWithCode.
- **Unofficial Implementation**: A community reproduction. Check the stars and recent activity to gauge quality.

## 4. Expected Output Format
Return a concise, direct answer to the user. Do not write a long essay. Always include the framework if you discovered it.

**If Official Code is Found:**
> ✅ **Official Implementation Found:**
> [Repository Name](URL)
> *(Implemented in [Framework])*

**If Only Unofficial Code is Found:**
> ⚠️ **No Official Code Found, but community implementations exist:**
> - [Repo Name](URL) (⭐ XXX) - Unofficial [Framework] implementation.

**If No Code Exists:**
> ❌ **No Code Found.** 
> I searched PapersWithCode, Hugging Face, direct GitHub, and the authors' profiles ([Author 1], [Author 2]), but could not find any public implementations.
