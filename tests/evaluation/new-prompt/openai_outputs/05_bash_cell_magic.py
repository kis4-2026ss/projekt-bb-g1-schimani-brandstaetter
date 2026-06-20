import marimo

__generated_with = "0.23.10"
app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo

    return (mo,)


@app.cell
def _cell_1(mo):
    mo.md(r"""
    # Bash cell magic
    """)
    return


@app.cell
def _cell_2():
    import subprocess as _subprocess
    import sys as _sys

    _result = _subprocess.run(
        """echo "hello from bash"
    ls""",
        shell=True,
        executable="/bin/bash",
        check=True,
        capture_output=True,
        text=True,
    )

    if _result.stdout:
        print(_result.stdout, end="")
    if _result.stderr:
        print(_result.stderr, end="", file=_sys.stderr)
    return


if __name__ == "__main__":
    app.run()
