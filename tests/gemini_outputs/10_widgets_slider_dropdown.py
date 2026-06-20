import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md(
        """
        # Widgets: slider, dropdown, and dependent output
        """
    ),


@app.cell
def _cell_1():
    import ipywidgets as widgets

    # The original notebook used ipywidgets, which can be wrapped by Marimo's mo.ui.ipywidget
    # to display them and access their values in Marimo.
    _slider_widget = widgets.IntSlider(value=3, min=1, max=10, description="Factor")
    _dropdown_widget = widgets.Dropdown(
        options=["small", "medium", "large"],
        value="medium",
        description="Size:",
    )

    # Wrap the ipywidgets for Marimo display and value access
    slider = mo.ui.ipywidget(_slider_widget)
    dropdown = mo.ui.ipywidget(_dropdown_widget)

    # Return the Marimo-wrapped widgets so their values can be accessed by dependent cells
    # and they are displayed in the Marimo notebook.
    return slider, dropdown


@app.cell
def _cell_2(dropdown, slider):
    # Access the current values of the widgets
    result = slider.value * 2
    print("selection:", dropdown.value)
    print("result:", result)
    # The 'result' variable is only used for printing within this cell
    # and is not needed by any subsequent cells, so it does not need to be returned.
    # Print statements are side-effects and will appear in the cell's output.
    return