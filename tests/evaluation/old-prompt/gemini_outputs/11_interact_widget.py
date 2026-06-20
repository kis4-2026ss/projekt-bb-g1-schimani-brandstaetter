import marimo as mo
app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# interact widget")

@app.cell
def _cell_1():
    from ipywidgets import interact

    def square(x):
        return x * x

    # This ipywidgets.interact call is placed here as-is
    # to preserve the original notebook cell's content.
    # Note: ipywidgets are not natively rendered as interactive
    # UI elements by Marimo. For Marimo-native interactivity,
    # consider using mo.ui components (e.g., mo.ui.slider).
    interact(square, x=(1, 10))
    return