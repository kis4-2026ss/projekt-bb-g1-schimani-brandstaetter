import os
import ast
import time
import subprocess
from typing import Dict, List, Any

import nbformat
import networkx as nx
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(".env")

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def fix_with_ai(code: str) -> str:
    """
    Converts notebook-specific syntax into valid Python.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": """
You are a Jupyter-to-Python migration tool.

Convert notebook-specific syntax into valid Python.

Examples:
- %timeit
- %cd
- %matplotlib inline
- !pip install ...
- !ls
- shell commands

Requirements:
- Preserve behavior as closely as possible.
- Return ONLY valid Python code.
- No markdown.
- No explanations.
"""
                },
                {
                    "role": "user",
                    "content": code
                }
            ]
        )

        result = response.choices[0].message.content

        result = result.replace("```python", "")
        result = result.replace("```", "")

        return result.strip()

    except Exception as e:
        raise RuntimeError(
            f"LLM normalization failed: {e}"
        )


def extract_defined(tree):
    return {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Store)
    }


def extract_used(tree):
    return {
        node.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Name)
        and isinstance(node.ctx, ast.Load)
    }


def extract_imports(tree):
    imports = []

    for node in ast.walk(tree):

        if isinstance(node, ast.Import):

            for alias in node.names:
                imports.append(alias.name)

        elif isinstance(node, ast.ImportFrom):

            module = node.module or ""

            for alias in node.names:
                imports.append(
                    f"{module}.{alias.name}"
                )

    return imports


def extract_functions(tree):
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef)
    ]


def extract_classes(tree):
    return [
        node.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ClassDef)
    ]



def analyze_code_cell(
    code: str,
    index: int
) -> Dict[str, Any]:

    tree = ast.parse(code)

    return {
        "cell_index": index,
        "cell_type": "code",
        "code": code,
        "defined": list(extract_defined(tree)),
        "used": list(extract_used(tree)),
        "imports": extract_imports(tree),
        "functions": extract_functions(tree),
        "classes": extract_classes(tree)
    }



def build_dependency_graph(cells_analysis):

    graph = nx.DiGraph()

    for cell in cells_analysis:
        graph.add_node(cell["cell_index"])

    for producer in cells_analysis:

        produced = set(producer["defined"])

        if not produced:
            continue

        for consumer in cells_analysis:

            if producer["cell_index"] == consumer["cell_index"]:
                continue

            required = set(consumer["used"])

            overlap = produced.intersection(required)

            if overlap:
                graph.add_edge(
                    producer["cell_index"],
                    consumer["cell_index"],
                    variables=list(overlap)
                )

    return graph



def generate_marimo_notebook(
    notebook_cells,
    analyzed_cells,
    dependency_graph
):

    prompt = """
You are a Marimo expert.

Generate a complete executable Marimo notebook.

Requirements:

1. Use:
   import marimo as mo
   app = mo.App()

2. Preserve notebook behavior.

3. Convert markdown cells into:
   mo.md(...)

4. Use one @app.cell per notebook cell.

5. Respect dependency relationships.

6. Variables produced by one cell must be
   returned and injected into dependent cells.

7. Return ONLY Python code.

No markdown.
No explanations.
"""

    prompt += "\n\n=================\n"
    prompt += "NOTEBOOK CELLS\n"
    prompt += "=================\n\n"

    for cell in notebook_cells:

        prompt += (
            f"\nCELL {cell['cell_index']}\n"
            f"TYPE: {cell['cell_type']}\n"
            f"{cell['source']}\n"
        )

    prompt += "\n\n=================\n"
    prompt += "ANALYSIS\n"
    prompt += "=================\n\n"

    for cell in analyzed_cells:

        prompt += (
            f"CELL {cell['cell_index']}\n"
            f"DEFINED: {cell['defined']}\n"
            f"USED: {cell['used']}\n"
            f"IMPORTS: {cell['imports']}\n"
            f"FUNCTIONS: {cell['functions']}\n"
            f"CLASSES: {cell['classes']}\n\n"
        )

    prompt += "\n=================\n"
    prompt += "DEPENDENCY GRAPH\n"
    prompt += "=================\n\n"

    for source, target in dependency_graph.edges():
        prompt += f"{source} -> {target}\n"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    code = response.choices[0].message.content

    code = code.replace("```python", "")
    code = code.replace("```", "")

    return code.strip()



def validate_python(code):

    try:
        ast.parse(code)
        return True

    except SyntaxError:
        return False


def validate_marimo_output(code):

    try:
        ast.parse(code)

    except SyntaxError as e:
        raise RuntimeError(
            f"Generated Marimo notebook invalid:\n{e}"
        )



def test_execution(path):

    try:

        result = subprocess.run(
            ["python", path],
            capture_output=True,
            text=True,
            timeout=60
        )

        return {
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }

    except Exception as e:

        return {
            "returncode": -1,
            "stdout": "",
            "stderr": str(e)
        }


def convert_notebook(
    input_file,
    output_file="output_notebook.py",
    run_test=True
):

    print("Loading notebook...")

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as f:

        nb = nbformat.read(
            f,
            as_version=4
        )

    notebook_cells = []

    analyzed_cells = []

    print("Processing cells...")

    for idx, cell in enumerate(nb.cells):

        if cell.cell_type == "markdown":

            notebook_cells.append(
                {
                    "cell_index": idx,
                    "cell_type": "markdown",
                    "source": cell.source
                }
            )

            continue

        code = cell.source

        try:

            ast.parse(code)

            normalized_code = code

            print(
                f"Cell {idx}: Python OK"
            )

        except SyntaxError:

            print(
                f"Cell {idx}: Normalizing via LLM..."
            )

            normalized_code = fix_with_ai(code)

            try:
                ast.parse(normalized_code)

            except SyntaxError as e:

                raise RuntimeError(
                    f"LLM produced invalid Python "
                    f"in cell {idx}\n{e}"
                )

            time.sleep(1)

        notebook_cells.append(
            {
                "cell_index": idx,
                "cell_type": "code",
                "source": normalized_code
            }
        )

        analysis = analyze_code_cell(
            normalized_code,
            idx
        )

        analyzed_cells.append(
            analysis
        )

    print("Building dependency graph...")

    graph = build_dependency_graph(
        analyzed_cells
    )

    print(
        f"Graph nodes: {graph.number_of_nodes()}"
    )

    print(
        f"Graph edges: {graph.number_of_edges()}"
    )

    print("Generating Marimo notebook...")

    marimo_code = generate_marimo_notebook(
        notebook_cells,
        analyzed_cells,
        graph
    )

    validate_marimo_output(
        marimo_code
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            marimo_code
        )

    print(
        f"Saved: {output_file}"
    )

    if run_test:

        print(
            "Running execution test..."
        )

        result = test_execution(
            output_file
        )

        print(
            "\n=== EXECUTION RESULT ==="
        )

        print(
            f"Return code: {result['returncode']}"
        )

        if result["stderr"]:
            print(
                result["stderr"]
            )

    print("\nDone.")


if __name__ == "__main__":

    convert_notebook(
        "test.ipynb",
        "output_notebook.py",
        run_test=True
    )