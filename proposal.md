# Proposal: AI-Assisted Conversion of Jupyter Notebooks to Marimo

## Team Members

* Daniel Brandstätter
* Jennifer Schimani

---

# Motivation

Jupyter Notebooks are widely used for data science, machine learning, and scientific computing. However, they allow arbitrary execution order of cells, which can lead to hidden dependencies and reduced reproducibility.

Marimo is a modern notebook environment that uses a reactive execution model based on explicit dependencies between cells. Converting existing Jupyter notebooks to Marimo can therefore improve maintainability and reproducibility.

While Marimo already provides a converter, notebooks often contain Jupyter-specific constructs such as magic commands, shell commands, widgets, and interactive elements that are difficult to transform using purely rule-based approaches. Large Language Models (LLMs) may provide a flexible mechanism for handling such constructs.

---

# Objective

The goal of this project is to investigate whether an AI-assisted pipeline can automatically convert Jupyter notebooks into equivalent Marimo notebooks.

The system should:

1. Parse Jupyter notebooks (`.ipynb`).
2. Transform notebook-specific constructs into a canonical Python representation using an LLM.
3. Perform static code analysis using Python's Abstract Syntax Tree (AST).
4. Extract dependencies between notebook cells and construct a dependency graph.
5. Generate an equivalent Marimo notebook using an LLM.

---

# Research Question

**Can LLM-based normalization combined with static dependency analysis improve the automatic conversion of Jupyter notebooks to Marimo compared to a direct LLM-based conversion approach?**

---

## Architecture

The proposed conversion pipeline consists of the following stages:

1. **Notebook Parsing**

   * The input `.ipynb` file is loaded and split into markdown and code cells.

2. **Python Validation**

   * Each code cell is parsed using Python's built-in AST parser.
   * Cells that can be parsed successfully are kept unchanged.
   * If a cell cannot be parsed, it is assumed to contain Jupyter-specific syntax (e.g., magic commands or shell commands).

3. **AI-Assisted Cell Normalization**

   * Cells that fail AST parsing are sent to a Large Language Model.
   * The LLM transforms the cell into valid Python while preserving its original behavior.
   * The resulting code is parsed again using the AST parser.

4. **Dependency Analysis**

   * After all code cells have been transformed into valid Python, AST analysis is used to extract:

     * defined variables
     * used variables
     * imports
     * function definitions
   * This information is used to construct a dependency graph between notebook cells.

5. **Marimo Generation**

   * The normalized notebook and the generated dependency graph are provided to a Large Language Model.
   * The model generates an equivalent Marimo notebook.

### Architecture Diagram



```
┌─────────────────────────────┐
│ Jupyter Notebook (.ipynb)   │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      Notebook Parser        │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Split into Code Cells    │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        AST Parsing          │
└───────┬─────────────┬───────┘
        │             │
        │ Success     │ Error
        │             │
        ▼             ▼
┌───────────────┐ ┌──────────────────┐
│ Valid Python  │ │ LLM Normalization│
└───────┬───────┘ └────────┬─────────┘
        │                  │
        └────────┬─────────┘
                 │
                 ▼
┌─────────────────────────────┐
│ Normalized Python Notebook  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Dependency Graph (AST)   │
└───────┬───────────────┬─────┘
        │               │
        ▼               ▼
        │    ┌─────────────────────┐
        └───►│ LLM Marimo Generator│
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │   Marimo Notebook   │
             └─────────────────────┘
```




# Evaluation

The generated notebooks will be evaluated using a small set of public Jupyter notebooks.

The following aspects will be considered:

* successful conversion
* syntactic correctness
* ability to execute in Marimo
* preservation of notebook functionality
* handling of notebook-specific constructs

Additionally, results may be compared against the converter provided by Marimo.

Two approaches will be evaluated:

---

# Project Plan

| Phase     | Description                                                   | Effort   |
| --------- | ------------------------------------------------------------- | -------- |
| 1         | Literature review and familiarization with Jupyter and Marimo | 2 h      |
| 2         | Notebook parser implementation                                | 2 h      |
| 3         | LLM-based normalization prototype                             | 3 h      |
| 4         | AST analysis and dependency graph extraction                  | 3 h      |
| 5         | LLM-based Marimo generation                                   | 3 h      |
| 6         | Evaluation on example notebooks                               | 2 h      |
| 7         | Documentation and presentation preparation                    | 2 h      |
| **Total** |                                                               | **17 h** |

---

# Risks

| Risk                                                          | Mitigation                                           |
| ------------------------------------------------------------- | ---------------------------------------------------- |
| LLM fails to correctly normalize notebook-specific constructs | Restrict evaluation to common Jupyter features       |
| Generated Marimo notebook is syntactically invalid            | Perform syntax validation and manual inspection      |
| Dependency extraction misses complex runtime dependencies     | Limit analysis to statically detectable dependencies |
| Limited time budget                                           | Focus on a proof-of-concept implementation           |

---

# Expected Outcome

The project will result in:

* a prototype Jupyter-to-Marimo converter
* an AI-assisted notebook normalization step
* automatic dependency graph extraction
* an evaluation of the effectiveness of combining static analysis and LLM-based transformation

---

# Technologies

* Python
* Jupyter Notebook (`.ipynb`)
* Python AST
* Marimo
* OpenAI API (or compatible LLM API)
* optional NetworkX (for dependency graph generation)
* GitHub
