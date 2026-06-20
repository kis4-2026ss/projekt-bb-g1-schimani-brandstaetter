[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5deAuAXI)

# Jupyter2Marimo

Convert Jupyter notebooks (`.ipynb`) into Marimo notebooks (`.py`) with:

- JSON parsing of notebook cells
- LLM normalization for notebook-specific syntax that is not valid Python
- AST-based cell analysis
- dependency graph generation
- LLM-based Marimo code generation

## Installation

Install the LLM client dependencies:

```powershell
python -m pip install -r requirements.txt
```

To open generated notebooks with Marimo and run the provided test notebooks, install the runtime packages as well:

```powershell
python -m pip install marimo pandas matplotlib ipywidgets
```

In WSL, use `python3` instead of `python` if only `python3` is available:

```bash
python3 -m pip install -r requirements.txt
python3 -m pip install marimo pandas matplotlib ipywidgets
```

## Environment

Create a `.env` file in the project root, next to `README.md`.

Gemini:

```text
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key_here
```

OpenAI:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key_here
```

Provider choices:

- `gemini`
- `openai`
- `chatgpt` as alias for OpenAI

## Models

Current defaults in `src/llm_generator.py`:

| Provider | Normalization model | Generation model |
| --- | --- | --- |
| Gemini | `gemini-2.5-flash-lite` | `gemini-2.5-flash` |
| OpenAI / ChatGPT | `gpt-5.5` | `gpt-5.5` |

Model overrides are possible through `.env`:

```text
GEMINI_NORMALIZATION_MODEL=gemini-2.5-flash-lite
GEMINI_GENERATION_MODEL=gemini-2.5-flash
OPENAI_NORMALIZATION_MODEL=gpt-5.5
OPENAI_GENERATION_MODEL=gpt-5.5
```

Or through CLI options:

```powershell
python src/converter.py tests/test_notebooks/01_basic_python_imports_functions.ipynb tests/marimo_outputs/01_basic_python_imports_functions.py --provider openai --generation-model gpt-5.5
```

## Convert One Notebook

Gemini:

```powershell
python src/converter.py tests/test_notebooks/01_basic_python_imports_functions.ipynb tests/marimo_outputs/01_basic_python_imports_functions.py --provider gemini
```

OpenAI:

```powershell
python src/converter.py tests/test_notebooks/01_basic_python_imports_functions.ipynb tests/marimo_outputs/01_basic_python_imports_functions.py --provider openai
```

Skip the generated Python execution test:

```powershell
python src/converter.py tests/test_notebooks/01_basic_python_imports_functions.ipynb tests/marimo_outputs/01_basic_python_imports_functions.py --provider openai --no-test
```

`--no-test` only skips running the generated `.py` file with Python. The Marimo file is still generated.

## Open A Generated Marimo Notebook

```powershell
python -m marimo edit tests/marimo_outputs/01_basic_python_imports_functions.py
```

In WSL:

```bash
python3 -m marimo edit tests/evaluation/new-prompt/openai_outputs/15_combined_jupyter_features.py
```

Some test notebooks contain Linux shell commands such as `ls`, `cat`, or `%%bash`. Those should be opened from WSL/Linux, not from plain Windows PowerShell.

## Run The Test Suite

Run all 15 test notebooks with the provider from `.env`:

```powershell
python tests/run_evaluation.py
```

Run all tests with a specific provider:

```powershell
python tests/run_evaluation.py --provider openai
python tests/run_evaluation.py --provider gemini
```

Run only a range:

```powershell
python tests/run_evaluation.py --provider openai --first 10 --last 15
```

The evaluator stops when a quota/token/rate-limit error is detected. To continue anyway:

```powershell
python tests/run_evaluation.py --provider openai --continue-on-quota
```

Evaluation results are written as `.csv` and `.md` files in `tests/evaluation`. Log files are written below `tests/evaluation/logs`.

## Test Notebooks

The generated test inputs are stored in:

```text
tests/test_notebooks
```

They cover:

- basic Python imports/functions
- timing magics
- Matplotlib plots
- file creation and CSV loading
- Bash/shell commands
- `%%writefile`
- HTML/DataFrame display
- widgets and `interact`
- `get_ipython`
- variable redefinition
- larger combined notebooks

Linux-specific shell behavior is not treated as a converter error when it comes from the original notebook. These tests should be run in WSL/Linux.

## Demo Notebooks

Demo input notebooks are in:

```text
demo/input-files-jupyter
```

Generated demo Marimo outputs are in:

```text
demo/outputs-files-marimo
  old-prompt/
  new-prompt/
```

The demo outputs are split by prompt version in the same way as the evaluation outputs. `old-prompt` contains demo conversions from the first prompt version. `new-prompt` contains demo conversions after the stricter Marimo prompt rules were added.

Example conversion:

```powershell
python src/converter.py demo/input-files-jupyter/small_demo.ipynb demo/outputs-files-marimo/new-prompt/small_demo.py --provider openai --no-test
```

## Project Structure

```text
src/
  converter.py
  json_parser.py
  ast_parser.py
  dependency_graph_builder.py
  llm_generator.py
  models.py

tests/
  test_notebooks/
  run_evaluation.py
  create_test_notebooks.py
  evaluation/

demo/
  input-files-jupyter/
  outputs-files-marimo/
```

## Evaluation Summary

The evaluation results are stored separately from the source notebooks and demo files. This keeps the original test cases unchanged and makes it possible to compare different prompt/provider runs.

Both tests and demos are separated by prompt version:

- `old-prompt`: outputs generated with the first prompt version
- `new-prompt`: outputs generated after improving the prompt in `src/llm_generator.py`

Evaluation folder structure:

```text
tests/evaluation/
  old-prompt/
    gemini_outputs/
    openai_outputs/
    logs/
    gemini_review_summary.md
    openai_review_summary.md

  new-prompt/
    openai_outputs/
    logs/
    openai_review_summary.md
```

`old-prompt` contains outputs generated before the prompt was improved. `new-prompt` contains outputs generated after adding stricter Marimo rules for imports, dependencies, widgets, display handling, file side effects, and Jupyter/IPython cleanup.

The prompt versions are also documented in `src/llm_generator.py`:

- `OLD_MARIMO_PROMPT_REFERENCE` keeps the old prompt rules as inactive reference.
- `NEW_MARIMO_PROMPT_RULES` and `NEW_MARIMO_CONVERSION_GUARDRAILS` are the active prompt rules used for new conversions.

Detailed review summaries:

- `tests/evaluation/old-prompt/gemini_review_summary.md`
- `tests/evaluation/old-prompt/openai_review_summary.md`
- `tests/evaluation/new-prompt/openai_review_summary.md`

These summaries were generated after a static Codex code review of the produced Marimo files. The review checked syntax, Marimo structure, dependency issues, remaining Jupyter/IPython-specific code, widget conversion, display conversion, and file side effects.

Short result:

- With the old prompt, the selected model made less difference than expected. The prompt itself had a much stronger impact on the output quality.
- Simply sending notebook code to an LLM and asking it to translate the code is not reliable enough for complex Jupyter features.
- Basic Jupyter magics were converted reasonably well, but widgets, rich display output, file side effects, and Marimo dependency rules required much more explicit instructions.
- The new prompt produced the best overall result because it tells the model which Jupyter constructs must be converted and which Marimo patterns should be used instead.

Possible improvement:

- Since the prompt has a strong impact on the result, a future version could add an intermediate analysis step before the final conversion. In that step, an LLM could inspect the notebook, identify which conversion rules are relevant, and generate a notebook-specific prompt. The final conversion could then use this tailored prompt instead of one fixed prompt for all notebooks.
