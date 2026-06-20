import marimo as mo

app = mo.App()


@app.cell
def _cell_0():
    return mo.md("# Variable redefinition across cells")


@app.cell
def _cell_1():
    # In a traditional notebook, 'x' would be defined globally and reassigned.
    # In Marimo, each cell defines its own scope for public variables.
    # We define x here, and make it a public variable as 'x_from_cell1'.
    # If the intent was to show a global redefinition, this would need a different pattern in Marimo.
    x_from_cell1 = 1
    print("first value:", x_from_cell1)
    return x_from_cell1,


@app.cell
def _cell_2(x_from_cell1):
    # This cell receives 'x_from_cell1' as input from the previous cell.
    # It then defines its own local variable named 'x' (or a new public variable
    # if returned) which effectively "redefines" the concept of 'x' for this cell.
    # We name the returned variable 'x_from_cell2' to avoid conflicts with
    # 'x_from_cell1' in Marimo's public variable namespace, as public variables
    # must be defined in exactly one cell.
    _ = x_from_cell1 # Acknowledging the dependency, but not using it for redefinition here.
    x_from_cell2 = 2
    print("second value:", x_from_cell2)
    return x_from_cell2,