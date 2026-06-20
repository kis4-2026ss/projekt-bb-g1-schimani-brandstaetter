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
    # In a Marimo environment, IPython magic commands like %matplotlib inline
    # are not directly supported. However, Marimo renders matplotlib plots
    # inline by default, so the effect of this command is preserved without
    # needing explicit execution. `get_ipython()` is not available in Marimo.
    pass

@app.cell
def _cell_2():
    import matplotlib.pyplot as plt

    plt.plot([1, 2, 3], [1, 4, 9])
    plt.show()
    return plt,