import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    mo.md("# Variable redefinition across cells")
    return

@app.cell
def _cell_1():
    x = 1
    print("first value:", x)
    return x,

@app.cell
def _cell_2(x):
    x = 2
    print("second value:", x)
    return x,