import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md(
        """
        # Shell commands with variables and captured output
        """
    )


@app.cell
def _cell_1():
    from pathlib import Path

    filename = "data.csv"
    Path(filename).write_text("a,b\n1,2\n", encoding="utf-8")
    Path("extra.csv").write_text("a,b\n3,4\n", encoding="utf-8")
    return filename, Path


@app.cell
def _cell_2():
    import subprocess

    subprocess.run(['ls'])
    return subprocess,


@app.cell
def _cell_3(filename, subprocess):
    subprocess.run(['cat', filename])
    return


@app.cell
def _cell_4():
    import glob
    import os

    files = glob.glob("*.csv")
    print(files)
    return