[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/5deAuAXI)

# Jupyter2Marimo

Convert a Jupyter notebook into a Marimo notebook with AST-based dependency
analysis and optional LLM normalization.

## Usage

```powershell
python src/converter.py tests/jupyter_input/test.ipynb tests/marimo_outputs/output_notebook.py --provider gemini
```

Provider choices:

- `gemini`: uses `GEMINI_API_KEY` or `GOOGLE_API_KEY`
- `chatgpt` / `openai`: uses `OPENAI_API_KEY`

You can also set the provider in `.env`:

```text
LLM_PROVIDER=gemini
GEMINI_API_KEY=...
OPENAI_API_KEY=...
```

Optional model overrides:

```powershell
python src/converter.py --provider chatgpt --normalization-model gpt-4o-mini --generation-model gpt-4o
python src/converter.py --provider gemini --normalization-model gemini-2.5-flash-lite --generation-model gemini-2.5-pro
```

Default test models:

- `chatgpt` / `openai`: `gpt-4o-mini` instead of the final-run model `gpt-4o`
- `gemini`: `gemini-2.5-flash-lite` instead of the final-run model `gemini-2.5-pro`
