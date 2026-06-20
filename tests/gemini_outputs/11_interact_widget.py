import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md(
        """
        # interact widget
        """
    ),


@app.cell
def _cell_1():
    from ipywidgets import interact

    def square(x):
        return x * x

    interact(square, x=(1, 10))
    return