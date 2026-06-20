import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    return mo,


@app.cell
def _cell_1(mo):
    mo.md(r"""# interact widget""")
    return


@app.cell
def _cell_2(mo):
    def square(x):
        return x * x

    x = mo.ui.slider(start=1, stop=10, step=1, value=1, label="x")
    return square, x


@app.cell
def _cell_3(mo, square, x):
    mo.vstack([x, mo.md(f"{square(x.value)}")])
    return


if __name__ == "__main__":
    app.run()