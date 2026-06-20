import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md(
        """
        # Variable redefinition across cells
        """
    )


@app.cell
def _cell_1(x_2):
    # This cell defines its own version of 'x', here named 'x_1' to satisfy
    # Marimo's rule that public variables must be defined in exactly one cell.
    # It receives 'x_2' as an input as per the dependency graph.
    x_1 = 1
    print("first value:", x_1)
    return x_1,


@app.cell
def _cell_2(x_1):
    # This cell defines its own version of 'x', here named 'x_2' to satisfy
    # Marimo's rule that public variables must be defined in exactly one cell.
    # It receives 'x_1' as an input as per the dependency graph.
    x_2 = 2
    print("second value:", x_2)
    return x_2,