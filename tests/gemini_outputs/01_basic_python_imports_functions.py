import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md(
        """
        # Basic Python, imports, functions, and data flow

        This notebook checks ordinary Python dependencies before any
        Jupyter-specific syntax is introduced.
        """
    )


@app.cell
def _cell_1():
    import pandas as pd
    from pathlib import Path
    base = 10
    return Path, base, pd


@app.cell
def _cell_2():
    def add_tax(value):
        return value * 1.2
    return add_tax,


@app.cell
def _cell_3(Path, add_tax, base, pd):
    df = pd.DataFrame({"value": [base, add_tax(base)]})
    current_path = Path(".")
    print(current_path.resolve())
    print(df)
    return current_path, df