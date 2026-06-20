import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return mo.md(
        """
        # get_ipython magic call
        """
    )

@app.cell
def _cell_1():
    # The `get_ipython().run_line_magic("matplotlib", "inline")` command
    # is specific to IPython/Jupyter notebooks for configuring plot display.
    # In a Marimo environment, matplotlib figures are rendered automatically,
    # and `get_ipython()` is not available, which would cause a NameError.
    # We use `pass` to maintain the cell structure while ensuring executability
    # and preserving the intended behavior of displaying plots.
    pass

@app.cell
def _cell_2():
    import matplotlib.pyplot as plt

    plt.plot([1, 2, 3], [1, 4, 9])
    plt.show()
    # No variables are returned as `plt` is not explicitly used by any subsequent cells
    # according to the provided dependency analysis.
    return