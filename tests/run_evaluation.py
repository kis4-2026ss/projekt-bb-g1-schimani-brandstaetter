from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "tests" / "test_notebooks"
EVALUATION_DIR = ROOT / "tests" / "evaluation"
LOG_DIR = EVALUATION_DIR / "logs"
VALID_PROVIDERS = {"gemini", "openai", "chatgpt"}

QUOTA_PATTERNS = (
    "quota",
    "insufficient_quota",
    "resource_exhausted",
    "rate limit",
    "rate_limit",
    "429",
    "no tokens",
    "token limit",
    "free tier",
)

MANUAL_REVIEW_REASONS = {
    3: "plot output should be visually checked",
    8: "HTML display should be visually checked",
    9: "DataFrame display should be checked in Marimo",
    10: "widgets require manual interaction check",
    11: "interact widget requires manual interaction check",
    13: "variable redefinition is a semantic Marimo/Jupyter difference",
    14: "large notebook with widgets, tables, and plots needs manual review",
    15: "large combined Jupyter-feature notebook needs manual review",
}


@dataclass
class EvaluationResult:
    test_id: int
    notebook: str
    output: str
    conversion: str
    python_syntax: str
    static_marimo_shape: str
    manual_review: str
    final_status: str
    notes: str
    log_file: str


def load_env(path: Path) -> dict[str, str]:
    values = {}

    if not path.exists():
        return values

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")

    return values


def provider_from_env(cli_provider: str | None) -> str:
    if cli_provider:
        return cli_provider.strip().lower()

    env_values = load_env(ROOT / ".env")
    return env_values.get("LLM_PROVIDER", os.getenv("LLM_PROVIDER", "gemini")).strip().lower()


def output_dir_for_provider(provider: str) -> Path:
    if provider not in VALID_PROVIDERS:
        valid = ", ".join(sorted(VALID_PROVIDERS))
        raise SystemExit(f"Unknown provider `{provider}`. Use one of: {valid}.")

    if provider in {"openai", "chatgpt"}:
        return ROOT / "tests" / "openai_outputs"

    return ROOT / "tests" / "gemini_outputs"


def test_id_from_path(path: Path) -> int:
    return int(path.name.split("_", 1)[0])


def unique_path(path: Path) -> Path:
    if not path.exists():
        return path

    counter = 1
    while True:
        candidate = path.with_name(f"{path.stem}_{counter}{path.suffix}")
        if not candidate.exists():
            return candidate

        counter += 1


def selected_notebooks(first: int, last: int) -> list[Path]:
    notebooks = sorted(NOTEBOOK_DIR.glob("*.ipynb"))
    return [
        path
        for path in notebooks
        if first <= test_id_from_path(path) <= last
    ]


def run_command(command: list[str], timeout_seconds: int) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return subprocess.CompletedProcess(
            args=command,
            returncode=124,
            stdout=exc.stdout or "",
            stderr=f"Command timed out after {timeout_seconds} seconds.",
        )


def contains_quota_error(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in QUOTA_PATTERNS)


def write_log(path: Path, command: list[str], result: subprocess.CompletedProcess) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                f"COMMAND: {' '.join(command)}",
                f"RETURN CODE: {result.returncode}",
                "",
                "STDOUT:",
                result.stdout,
                "",
                "STDERR:",
                result.stderr,
            ]
        ),
        encoding="utf-8",
    )


def check_python_syntax(output_path: Path) -> tuple[str, str]:
    if not output_path.exists():
        return "SKIP", "output file missing"

    result = run_command(
        [sys.executable, "-m", "py_compile", str(output_path)],
        timeout_seconds=30,
    )

    if result.returncode == 0:
        return "PASS", ""

    return "FAIL", (result.stderr or result.stdout).strip()


def check_static_marimo_shape(output_path: Path) -> tuple[str, str]:
    if not output_path.exists():
        return "SKIP", "output file missing"

    code = output_path.read_text(encoding="utf-8")
    missing = []

    if "import marimo" not in code:
        missing.append("missing marimo import")

    if "mo.App(" not in code and "marimo.App(" not in code:
        missing.append("missing app creation")

    if "@app.cell" not in code:
        missing.append("missing @app.cell")

    if missing:
        return "WARN", "; ".join(missing)

    return "PASS", ""


def manual_review_reason(test_id: int) -> str:
    return MANUAL_REVIEW_REASONS.get(test_id, "")


def evaluate_notebook(
    notebook_path: Path,
    output_dir: Path,
    provider: str,
    timeout_seconds: int,
) -> tuple[EvaluationResult, bool]:
    test_id = test_id_from_path(notebook_path)
    output_path = output_dir / f"{notebook_path.stem}.py"
    log_path = unique_path(LOG_DIR / provider / f"{notebook_path.stem}.log")

    if output_path.exists():
        output_path.unlink()

    command = [
        sys.executable,
        "src/converter.py",
        str(notebook_path),
        str(output_path),
        "--provider",
        provider,
        "--no-test",
    ]

    result = run_command(command, timeout_seconds=timeout_seconds)
    write_log(log_path, command, result)

    combined_output = f"{result.stdout}\n{result.stderr}"
    quota_error = contains_quota_error(combined_output)

    if result.returncode == 0 and output_path.exists():
        conversion = "PASS"
        notes = ""
    elif quota_error:
        conversion = "STOPPED_QUOTA"
        notes = "quota or token limit reached"
    else:
        conversion = "FAIL"
        notes = first_relevant_line(combined_output)

    python_syntax, syntax_notes = check_python_syntax(output_path)
    static_shape, shape_notes = check_static_marimo_shape(output_path)
    review_reason = manual_review_reason(test_id)
    manual_review = "YES" if review_reason else "NO"

    all_notes = "; ".join(
        note
        for note in [notes, syntax_notes, shape_notes, review_reason]
        if note
    )

    if conversion == "STOPPED_QUOTA":
        final_status = "STOPPED_QUOTA"
    elif conversion != "PASS" or python_syntax == "FAIL":
        final_status = "AUTO_FAIL"
    elif manual_review == "YES" or static_shape == "WARN":
        final_status = "MANUAL_REVIEW"
    else:
        final_status = "AUTO_PASS"

    return (
        EvaluationResult(
            test_id=test_id,
            notebook=notebook_path.name,
            output=str(output_path.relative_to(ROOT)),
            conversion=conversion,
            python_syntax=python_syntax,
            static_marimo_shape=static_shape,
            manual_review=manual_review,
            final_status=final_status,
            notes=all_notes,
            log_file=str(log_path.relative_to(ROOT)),
        ),
        quota_error,
    )


def first_relevant_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if "Reason:" in stripped or "failed" in stripped.lower() or "error" in stripped.lower():
            return stripped

    return "conversion failed"


def write_results_csv(path: Path, results: list[EvaluationResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=list(EvaluationResult.__dataclass_fields__.keys()),
            delimiter=";",
        )
        writer.writeheader()
        for result in results:
            writer.writerow(result.__dict__)


def write_results_markdown(path: Path, provider: str, results: list[EvaluationResult]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        f"# Evaluation Results ({provider})",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "| Test | Notebook | Conversion | Python | Shape | Manual | Status | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]

    for result in results:
        lines.append(
            "| "
            + " | ".join(
                [
                    str(result.test_id),
                    result.notebook,
                    result.conversion,
                    result.python_syntax,
                    result.static_marimo_shape,
                    result.manual_review,
                    result.final_status,
                    result.notes.replace("|", "\\|"),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Status meaning",
            "",
            "- `AUTO_PASS`: automatic checks passed and no mandatory manual review is marked.",
            "- `MANUAL_REVIEW`: automatic checks passed, but visual/interactive/semantic review is needed.",
            "- `AUTO_FAIL`: conversion or automatic checks failed.",
            "- `STOPPED_QUOTA`: token/quota/rate-limit condition detected; following tests were skipped.",
        ]
    )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_summary(results: list[EvaluationResult]) -> None:
    counts = {}
    for result in results:
        counts[result.final_status] = counts.get(result.final_status, 0) + 1

    print("\n=== Evaluation Summary ===")
    for status in ["AUTO_PASS", "MANUAL_REVIEW", "AUTO_FAIL", "STOPPED_QUOTA"]:
        print(f"{status}: {counts.get(status, 0)}")

    print("\nDetailed results:")
    for result in results:
        print(
            f"{result.test_id:02d} {result.final_status:14} "
            f"{result.notebook} "
            f"(conversion={result.conversion}, python={result.python_syntax}, manual={result.manual_review})"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the generated Jupyter-to-Marimo evaluation notebooks."
    )
    parser.add_argument("--first", type=int, default=1, help="First test id to run.")
    parser.add_argument("--last", type=int, default=15, help="Last test id to run.")
    parser.add_argument(
        "--provider",
        choices=["gemini", "openai", "chatgpt"],
        default=None,
        help="Override LLM provider from .env.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=240,
        help="Timeout per conversion in seconds.",
    )
    parser.add_argument(
        "--continue-on-quota",
        action="store_true",
        help="Do not stop when a quota/token/rate-limit error is detected.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    provider = provider_from_env(args.provider)

    if args.first > args.last:
        raise SystemExit("--first must be smaller than or equal to --last.")

    output_dir = output_dir_for_provider(provider)
    output_dir.mkdir(parents=True, exist_ok=True)

    notebooks = selected_notebooks(args.first, args.last)

    if not notebooks:
        raise SystemExit("No notebooks selected.")

    print(f"Provider: {provider}")
    print(f"Output directory: {output_dir.relative_to(ROOT)}")
    print(f"Selected tests: {args.first}..{args.last}")

    results = []

    for notebook_path in notebooks:
        test_id = test_id_from_path(notebook_path)
        print(f"\n=== Running test {test_id:02d}: {notebook_path.name} ===")

        result, quota_error = evaluate_notebook(
            notebook_path=notebook_path,
            output_dir=output_dir,
            provider=provider,
            timeout_seconds=args.timeout,
        )
        results.append(result)
        print(f"Result: {result.final_status}")

        if quota_error and not args.continue_on_quota:
            print("Quota/token/rate-limit condition detected. Stopping remaining tests.")
            break

    csv_path = unique_path(EVALUATION_DIR / f"{provider}_results.csv")
    markdown_path = unique_path(EVALUATION_DIR / f"{provider}_results.md")
    write_results_csv(csv_path, results)
    write_results_markdown(markdown_path, provider, results)
    print_summary(results)

    print(f"\nWrote {csv_path.relative_to(ROOT)}")
    print(f"Wrote {markdown_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
