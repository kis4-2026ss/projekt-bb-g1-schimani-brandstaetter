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
    return filename,


@app.cell
def _cell_subprocess_init():
    # To adhere to the rule "Public variable names must be defined in exactly one cell",
    # subprocess is imported here and returned, then passed to dependent cells.
    # This also resolves the conflicting circular dependency stated in the analysis
    # for 'subprocess' by providing a single source for the module object.
    import subprocess
    return subprocess,


@app.cell
def _cell_2(subprocess):
    subprocess.run(["ls"])
    return


@app.cell
def _cell_3(filename, subprocess):
    subprocess.run(['cat', filename])
    return


@app.cell
def _cell_4():
    import os
    files = [f for f in os.listdir('.') if f.endswith('.csv')]
    print(files)
    return