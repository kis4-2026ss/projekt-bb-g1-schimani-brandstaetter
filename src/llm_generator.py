from __future__ import annotations

import os
import time
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum
from typing import Any

from models import CodeCellAnalysis, DependencyGraph, NotebookCell

OPENAI_TEST_MODEL = "gpt-5.5"
GEMINI_NORMALIZATION_MODEL = "gemini-2.5-flash-lite"
GEMINI_GENERATION_MODEL = "gemini-2.5-flash"  # Actual model for final runs: gemini-2.5-pro

# Inactive old prompt reference kept for documentation and comparison.
# The active prompt uses NEW_MARIMO_PROMPT_RULES below.
OLD_MARIMO_PROMPT_REFERENCE = (
    "1. Use `import marimo as mo` and `app = mo.App()`.",
    "2. Preserve notebook behavior.",
    "3. Convert markdown cells into `mo.md(...)`.",
    "4. Use one `@app.cell` per notebook cell.",
    "5. Respect dependency relationships.",
    "6. Variables produced by a cell that are needed by other cells MUST be explicitly returned at the end of the function.",
    "7. CRUCIAL: If a cell returns only ONE variable, it MUST end with a trailing comma.",
    "8. Do not call decorated cell functions directly.",
    "9. Public variable names must be defined in exactly one cell.",
    "10. A dependent cell must receive values through function parameters.",
    "11. Cell function names must be unique private placeholders.",
    "12. Return ONLY Python code. No markdown. No explanations.",
)

NEW_MARIMO_PROMPT_RULES = (
    "1. Use module-level `import marimo` and `app = marimo.App()`.",
    "   If cells need the `mo` API, provide it through an import cell:",
    "   @app.cell",
    "   def _imports():",
    "       import marimo as mo",
    "       return mo,",
    "2. Preserve notebook behavior.",
    "3. Convert markdown cells into `mo.md(...)`.",
    "4. Use one `@app.cell` per notebook cell.",
    "5. Respect dependency relationships.",
    "6. Variables produced by a cell that are needed by other cells MUST be explicitly returned at the end of the function.",
    "7. CRUCIAL: If a cell returns only ONE variable, it MUST end with a trailing comma (e.g., `return my_var,`).",
    "8. Do not call decorated cell functions directly. Never write code like `x = __()`, `x = _()`, or `x = __init__()`.",
    "9. Public variable names must be defined in exactly one cell. If a local helper variable is needed, prefix it with `_`.",
    "10. A dependent cell must receive values through function parameters, for example `def _(x): print(x)`.",
    "11. Cell function names must be unique private placeholders such as `_cell_0`, `_cell_1`, `_cell_2`; they are not notebook APIs.",
    "12. Return ONLY Python code. No markdown. No explanations. No Jupyter specific code, only Marimo.",
)

NEW_MARIMO_CONVERSION_GUARDRAILS = (
    "Important Marimo conversion rules:",
    "- Do not preserve Jupyter/IPython-specific APIs. Never use `get_ipython`, `%...` magics, `!...` shell syntax, `IPython.display.display`, `IPython.display.HTML`, or `ipywidgets` in the generated output.",
    "- Convert `display(df)` by making the object a Marimo cell output, for example by returning `df` or a named preview variable.",
    "- Convert `display(HTML(...))` to `mo.Html(...)`.",
    "- Convert `ipywidgets` controls to Marimo controls, e.g. `widgets.IntSlider` to `mo.ui.slider` and `widgets.Dropdown` to `mo.ui.dropdown`.",
    "- If a cell creates visible Marimo UI/output objects such as `mo.Html(...)`, `mo.vstack(...)`, `mo.ui.*`, tables, or reports, ensure they are visible in Marimo and do not discard them.",
    "- For file-writing side effects, return a small sentinel variable such as `file_written = True`; file-reading cells should depend on that sentinel to preserve execution order.",
    "- Imports required by a cell must either be inside that same cell or provided by an earlier import cell and passed through parameters. Do not require a parameter before any cell returns it.",
    "- Do not call decorated cell functions manually. Let Marimo manage cell execution.",
    "- Preserve the original notebook behavior, but output idiomatic Marimo code rather than Jupyter-compatible fallback code.",
)


class LLMProvider(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"
    CHATGPT = "chatgpt"


@dataclass(frozen=True)
class LLMResponse:
    text: str


class LLMClient:
    def generate(self, prompt: str, model: str) -> LLMResponse:
        raise NotImplementedError


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str | None = None) -> None:
        try:
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError("OpenAI requires the `openai` package.") from exc

        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: str, model: str) -> LLMResponse:
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )

        return LLMResponse(text=response.choices[0].message.content or "")


class GeminiClient(LLMClient):
    def __init__(self, api_key: str | None = None, max_retries: int = 2) -> None:
        try:
            from google import genai
        except ImportError as exc:
            raise RuntimeError("Gemini requires the `google-genai` package.") from exc

        self.client = genai.Client(
            api_key=api_key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        )
        self.max_retries = max_retries

    def generate(self, prompt: str, model: str) -> LLMResponse:
        for attempt in range(self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                )
                return LLMResponse(text=response.text or "")
            except Exception:
                if attempt == self.max_retries:
                    raise

                time.sleep(2**attempt)


class LLMGenerator:
    def __init__(
        self,
        client: LLMClient | Any | None = None,
        provider: str | LLMProvider | None = None,
        normalization_model: str | None = None,
        generation_model: str | None = None,
    ) -> None:
        self._load_environment()
        self.provider = self._normalize_provider(provider)
        self.client = client or self._create_default_client(self.provider)
        self.normalization_model = normalization_model or self._default_normalization_model(
            self.provider
        )
        self.generation_model = generation_model or self._default_generation_model(
            self.provider
        )

    def _normalize_provider(self, provider: str | LLMProvider | None) -> LLMProvider:
        value = provider or os.getenv("LLM_PROVIDER", LLMProvider.GEMINI.value)

        try:
            return LLMProvider(value.lower())
        except ValueError as exc:
            valid = ", ".join(provider.value for provider in LLMProvider)
            raise ValueError(f"Unknown LLM provider `{value}`. Use one of: {valid}.") from exc

    def _create_default_client(self, provider: LLMProvider) -> LLMClient:
        if provider in {LLMProvider.OPENAI, LLMProvider.CHATGPT}:
            return OpenAIClient()

        return GeminiClient()

    def _load_environment(self) -> None:
        try:
            from dotenv import load_dotenv
        except ImportError:
            self._load_dotenv_fallback()
        else:
            load_dotenv(".env")

    def _load_dotenv_fallback(self) -> None:
        env_path = ".env"

        if not os.path.exists(env_path):
            return

        with open(env_path, encoding="utf-8") as env_file:
            for line in env_file:
                line = line.strip()

                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

    def _default_normalization_model(self, provider: LLMProvider) -> str:
        if provider in {LLMProvider.OPENAI, LLMProvider.CHATGPT}:
            return os.getenv("OPENAI_NORMALIZATION_MODEL", OPENAI_TEST_MODEL)

        return os.getenv("GEMINI_NORMALIZATION_MODEL", GEMINI_NORMALIZATION_MODEL)

    def _default_generation_model(self, provider: LLMProvider) -> str:
        if provider in {LLMProvider.OPENAI, LLMProvider.CHATGPT}:
            return os.getenv("OPENAI_GENERATION_MODEL", OPENAI_TEST_MODEL)

        return os.getenv("GEMINI_GENERATION_MODEL", GEMINI_GENERATION_MODEL)

    def normalize_cell(self, code: str) -> str:
        prompt = (
            "You are a Jupyter-to-Python migration tool.\n\n"
            "Convert notebook-specific syntax into valid Python.\n\n"
            "Examples:\n"
            "- %timeit\n"
            "- %cd\n"
            "- %matplotlib inline\n"
            "- !pip install ...\n"
            "- !ls\n"
            "- shell commands\n\n"
            "Requirements:\n"
            "- Preserve behavior as closely as possible.\n"
            "- Return ONLY valid Python code.\n"
            "- No markdown.\n"
            "- No explanations.\n\n"
            "Code:\n"
            f"{code}"
        )

        try:
            response = self.client.generate(prompt, self.normalization_model)
        except Exception as exc:
            raise RuntimeError(
                f"LLM normalization failed: {self._format_llm_error(exc)}"
            ) from exc

        return self._strip_code_fence(response.text)

    def generate_marimo_notebook(
        self,
        notebook_cells: Sequence[NotebookCell],
        analyzed_cells: Sequence[CodeCellAnalysis],
        dependency_graph: DependencyGraph,
    ) -> str:
        try:
            response = self.client.generate(
                self._build_marimo_prompt(
                    notebook_cells,
                    analyzed_cells,
                    dependency_graph,
                ),
                self.generation_model,
            )
        except Exception as exc:
            raise RuntimeError(
                f"LLM Marimo generation failed: {self._format_llm_error(exc)}"
            ) from exc

        return self._strip_code_fence(response.text)

    def _format_llm_error(self, exc: Exception) -> str:
        message = str(exc)

        if "503" in message and "UNAVAILABLE" in message:
            return (
                "503 UNAVAILABLE - the selected model is temporarily overloaded. "
                "Please try again later or switch to another model."
            )

        if "API_KEY" in message or "api_key" in message:
            return "API key is missing or invalid. Check your .env file."

        return message

    def _build_marimo_prompt(
        self,
        notebook_cells: Sequence[NotebookCell],
        analyzed_cells: Sequence[CodeCellAnalysis],
        dependency_graph: DependencyGraph,
    ) -> str:
        prompt = [
            "You are a Marimo expert.",
            "",
            "Generate a complete executable Marimo notebook.",
            "",
            "Requirements:",
            *NEW_MARIMO_PROMPT_RULES,
            "",
            *NEW_MARIMO_CONVERSION_GUARDRAILS,
            "",
            "Correct dependency example:",
            "@app.cell",
            "def _():",
            "    x = 10",
            "    return x,",
            "",
            "@app.cell",
            "def __(x):",
            "    print(x)",
            "    return",
            "",
            "Incorrect example:",
            "@app.cell",
            "def __():",
            "    x = _()",
            "    print(x)",
            "    return",
            "",
            "=================",
            "NOTEBOOK CELLS",
            "=================",
        ]

        for cell in notebook_cells:
            prompt.extend(
                [
                    "",
                    f"CELL {cell.index}",
                    f"TYPE: {cell.cell_type}",
                    cell.source,
                ]
            )

        prompt.extend(
            [
                "",
                "=================",
                "ANALYSIS",
                "=================",
                "",
            ]
        )

        for analysis in analyzed_cells:
            prompt.extend(
                [
                    f"CELL {analysis.cell_index}",
                    f"DEFINED: {sorted(analysis.defined)}",
                    f"USED: {sorted(analysis.used)}",
                    f"IMPORTS: {analysis.imports}",
                    f"FUNCTIONS: {analysis.functions}",
                    f"CLASSES: {analysis.classes}",
                    "",
                ]
            )

        prompt.extend(
            [
                "=================",
                "DEPENDENCY GRAPH (EXACT VARIABLES)",
                "=================",
                "",
            ]
        )

        for edge in dependency_graph.dependency_edges:
            variables = ", ".join(edge.variables)
            prompt.append(f"Cell {edge.source} MUST pass these variables to Cell {edge.target}: [{variables}]")

        prompt.extend([
            "",
            "STRICT RULES FOR GENERATION:",
            "1. Each cell function MUST accept the variables listed above as arguments.",
            "2. Example: If Cell 0 passes ['df'] to Cell 1, Cell 1 MUST be 'def _(df):'"
        ])

        return "\n".join(prompt)

    def _strip_code_fence(self, code: str) -> str:
        return code.replace("```python", "").replace("```", "").strip()

