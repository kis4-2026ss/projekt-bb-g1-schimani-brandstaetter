import marimo

app = marimo.App()


@app.cell
def _imports():
    import marimo as mo

    return mo,


@app.cell
def _cell_0(mo):
    mo.md(r"""# get_ipython magic call""")
    return


@app.cell
def _cell_1():
    # Jupyter-specific matplotlib inline magic is not needed in Marimo.
    return


@app.cell
def _cell_2():
    import matplotlib.pyplot as _plt

    _fig, _ax = _plt.subplots()
    _ax.plot([1, 2, 3], [1, 4, 9])
    _fig
    return


if __name__ == "__main__":
    app.run()