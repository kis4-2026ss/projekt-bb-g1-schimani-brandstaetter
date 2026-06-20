import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# Widgets: slider, dropdown, and dependent output"),

@app.cell
def _cell_1():
    import ipywidgets as widgets
    from IPython.display import display

    slider = widgets.IntSlider(value=3, min=1, max=10, description="Factor")
    dropdown = widgets.Dropdown(
        options=["small", "medium", "large"],
        value="medium",
        description="Size:",
    )

    display(slider)
    display(dropdown)

    return slider, dropdown,

@app.cell
def _cell_2(slider, dropdown):
    result = slider.value * 2
    print("selection:", dropdown.value)
    print("result:", result)

    return result,