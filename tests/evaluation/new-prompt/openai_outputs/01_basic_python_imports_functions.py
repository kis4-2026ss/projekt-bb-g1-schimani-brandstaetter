import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    return mo,


@app.cell
def _cell_1(mo):
    mo.md(
        r"""
        # Basic Python, imports, functions, and data flow

        This notebook checks ordinary Python dependencies before any
        Jupyter-specific syntax is introduced.
        """
    )
    return


@app.cell
def _cell_2():
    import pandas as pd
    from pathlib import Path

    base = 10
    return Path, base, pd


@app.cell
def _cell_3():
    def add_tax(value):
        return value * 1.2

    return add_tax,


@app.cell
def _cell_4(Path, add_tax, base, pd):
    df = pd.DataFrame({"value": [base, add_tax(base)]})
    current_path = Path(".")
    print(current_path.resolve())
    print(df)
    return current_path, df


if __name__ == "__main__":
    app.run()