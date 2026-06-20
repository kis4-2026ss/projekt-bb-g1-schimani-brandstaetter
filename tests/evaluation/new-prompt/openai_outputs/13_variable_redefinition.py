import marimo

app = marimo.App()


@app.cell
def _imports():
    import marimo as mo

    return mo,


@app.cell
def _cell_0(mo):
    mo.md(r"""# Variable redefinition across cells""")
    return


@app.cell
def _cell_1():
    class _MutableValue:
        def __init__(self, value):
            self.value = value

        def __str__(self):
            return str(self.value)

        def __repr__(self):
            return repr(self.value)

        def __int__(self):
            return int(self.value)

        def __float__(self):
            return float(self.value)

        def __eq__(self, other):
            return self.value == other

    x = _MutableValue(1)
    print("first value:", x)
    return x,


@app.cell
def _cell_2(x):
    x.value = 2
    print("second value:", x)
    return


if __name__ == "__main__":
    app.run()