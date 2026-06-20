import marimo as mo
app = mo.App()

@app.cell
def _cell_0():
    return mo.md(
        """
        # Bash cell magic
        """
    )

@app.cell
def _cell_1():
    import subprocess
    subprocess.run(['echo "hello from bash"'], shell=True)
    subprocess.run(['ls'], shell=True)
    return