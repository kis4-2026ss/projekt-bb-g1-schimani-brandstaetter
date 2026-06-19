from __future__ import annotations

import argparse
import subprocess
import sys
import time
from pathlib import Path

from ast_parser import AstParser
from dependency_graph_builder import DependencyGraphBuilder
from jupyter_normalizer import JupyterNormalizer
from json_parser import JsonParser
from llm_generator import LLMGenerator
from models import CodeCellAnalysis, NotebookCell


class NotebookConverter:
    def __init__(
        self,
        json_parser: JsonParser | None = None,
        ast_parser: AstParser | None = None,
        graph_builder: DependencyGraphBuilder | None = None,
        llm_generator: LLMGenerator | None = None,
        jupyter_normalizer: JupyterNormalizer | None = None,
        llm_delay_seconds: float = 1.0,
    ) -> None:
        self.json_parser = json_parser or JsonParser()
        self.ast_parser = ast_parser or AstParser()
        self.graph_builder = graph_builder or DependencyGraphBuilder()
        self.llm_generator = llm_generator or LLMGenerator()
        self.jupyter_normalizer = jupyter_normalizer or JupyterNormalizer()
        self.llm_delay_seconds = llm_delay_seconds

    def convert(
        self,
        input_file: str | Path,
        output_file: str | Path = "output_notebook.py",
        run_test: bool = True,
    ) -> None:
        print("Loading notebook...")
        notebook = self.json_parser.parse(input_file)

        print("Processing cells...")
        normalized_cells, analyzed_cells = self._normalize_and_analyze(notebook.cells)

        print("Building dependency graph...")
        graph = self.graph_builder.build(analyzed_cells)
        print(f"Graph nodes: {graph.number_of_nodes()}")
        print(f"Graph edges: {graph.number_of_edges()}")

        print("Generating Marimo notebook...")
        marimo_code = self.llm_generator.generate_marimo_notebook(
            normalized_cells,
            analyzed_cells,
            graph,
        )
        self.ast_parser.validate_marimo_output(marimo_code)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(marimo_code, encoding="utf-8")
        print(f"Saved: {output_path}")

        if run_test:
            print("Running execution test...")
            result = self.test_execution(output_path)
            print("\n=== EXECUTION RESULT ===")
            print(f"Return code: {result['returncode']}")

            if result["stderr"]:
                print(result["stderr"])

        print("\nDone.")

    def _normalize_and_analyze(
        self,
        cells: list[NotebookCell],
    ) -> tuple[list[NotebookCell], list[CodeCellAnalysis]]:
        normalized_cells = []
        analyzed_cells = []

        for cell in cells:
            if cell.is_markdown:
                normalized_cells.append(cell)
                continue

            normalized_cell = self._normalize_code_cell(cell)
            normalized_cells.append(normalized_cell)
            analyzed_cells.append(self.ast_parser.analyze_code_cell(normalized_cell))

        return normalized_cells, analyzed_cells

    def _normalize_code_cell(self, cell: NotebookCell) -> NotebookCell:
        if self.ast_parser.validate_python(cell.source):
            print(f"Cell {cell.index}: Python OK")
            return cell

        rule_based_code = self.jupyter_normalizer.normalize(cell.source)

        if rule_based_code and self.ast_parser.validate_python(rule_based_code):
            print(f"Cell {cell.index}: Normalized by rule")
            return NotebookCell(
                index=cell.index,
                cell_type=cell.cell_type,
                source=rule_based_code,
                metadata=cell.metadata,
            )

        print(f"Cell {cell.index}: Normalizing via LLM...")
        normalized_code = self.llm_generator.normalize_cell(cell.source)

        if not self.ast_parser.validate_python(normalized_code):
            raise RuntimeError(f"LLM produced invalid Python in cell {cell.index}")

        time.sleep(self.llm_delay_seconds)

        return NotebookCell(
            index=cell.index,
            cell_type=cell.cell_type,
            source=normalized_code,
            metadata=cell.metadata,
        )

    def test_execution(self, path: str | Path) -> dict[str, str | int]:
        try:
            result = subprocess.run(
                ["python", str(path)],
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )

            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        except Exception as exc:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(exc),
            }


def convert_notebook(
    input_file: str | Path,
    output_file: str | Path = "output_notebook.py",
    run_test: bool = True,
    provider: str | None = None,
    normalization_model: str | None = None,
    generation_model: str | None = None,
) -> None:
    llm_generator = LLMGenerator(
        provider=provider,
        normalization_model=normalization_model,
        generation_model=generation_model,
    )
    NotebookConverter(llm_generator=llm_generator).convert(
        input_file,
        output_file,
        run_test=run_test,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a Jupyter notebook to Marimo.")
    parser.add_argument(
        "input_file",
        nargs="?",
        default="tests/jupyter_input/test.ipynb",
        help="Path to the input .ipynb file.",
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="tests/marimo_outputs/output_notebook.py",
        help="Path for the generated Marimo notebook.",
    )
    parser.add_argument(
        "--no-test",
        action="store_true",
        help="Skip executing the generated notebook.",
    )
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai", "chatgpt"],
        default=None,
        help="LLM provider. Defaults to LLM_PROVIDER from .env or gemini.",
    )
    parser.add_argument(
        "--normalization-model",
        default=None,
        help="Model used to normalize invalid notebook cells.",
    )
    parser.add_argument(
        "--generation-model",
        default=None,
        help="Model used to generate the Marimo notebook.",
    )
    args = parser.parse_args()

    try:
        convert_notebook(
            args.input_file,
            args.output_file,
            run_test=not args.no_test,
            provider=args.provider,
            normalization_model=args.normalization_model,
            generation_model=args.generation_model,
        )
    except RuntimeError as exc:
        print("\nConversion aborted.")
        print(f"Reason: {exc}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nConversion aborted by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
