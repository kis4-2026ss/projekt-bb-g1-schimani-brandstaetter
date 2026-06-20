import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    return mo,


@app.cell
def _cell_1(mo):
    mo.md("# Matplotlib inline plot")
    return


@app.cell
def _cell_2():
    import matplotlib.pyplot as plt

    _values = [1, 4, 9, 16]
    _fig, _ax = plt.subplots()
    _ax.plot(_values, marker="o")
    _ax.set_title("Square values")
    _fig
    return


if __name__ == "__main__":
    app.run()