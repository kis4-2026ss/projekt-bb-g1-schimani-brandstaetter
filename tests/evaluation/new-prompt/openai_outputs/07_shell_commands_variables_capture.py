import marimo

app = marimo.App()


@app.cell
def _imports():
    import marimo as mo
    from pathlib import Path
    import subprocess
    import sys

    _markdown = mo.md(r"""# Shell commands with variables and captured output""")
    _markdown
    return Path, mo, subprocess, sys


@app.cell
def _cell_1(Path):
    filename = "data.csv"
    Path(filename).write_text("a,b\n1,2\n", encoding="utf-8")
    Path("extra.csv").write_text("a,b\n3,4\n", encoding="utf-8")
    file_written = True
    return file_written, filename


@app.cell
def _cell_2(file_written, subprocess):
    if file_written:
        subprocess.run("ls", shell=True, check=False)
    ls_completed = True
    return ls_completed,


@app.cell
def _cell_3(file_written, filename, ls_completed):
    if file_written and ls_completed:
        with open(filename, "r") as _f:
            print(_f.read(), end="")
    read_done = True
    return read_done,


@app.cell
def _cell_4(file_written, files, ls_completed, read_done, subprocess, sys):
    return


@app.cell
def _cell_5(file_written, ls_completed, read_done, subprocess, sys):
    _ = (file_written, ls_completed, read_done)
    _result = subprocess.run(
        "ls *.csv",
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if _result.stderr:
        print(_result.stderr, end="", file=sys.stderr)
    files = _result.stdout.splitlines()
    print(files)
    return files,


if __name__ == "__main__":
    app.run()