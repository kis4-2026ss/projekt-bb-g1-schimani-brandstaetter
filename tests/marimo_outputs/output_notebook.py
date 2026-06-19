import marimo

__generated_with = "0.23.10"
app = marimo.App()


@app.cell
def _cell_0():
    import timeit
    x = 700
    _timeit_result = timeit.timeit('x = 10', number=1000000)
    print(_timeit_result)
    return (x,)


@app.cell
def _cell_1():
    print("Hallo Welt")
    return


@app.cell
def _(x):
    print(x)
    return


if __name__ == "__main__":
    app.run()
