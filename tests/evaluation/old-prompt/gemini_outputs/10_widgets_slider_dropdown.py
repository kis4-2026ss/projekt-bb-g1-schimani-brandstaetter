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
    slider = mo.ui.slider(start=1, stop=10, value=3, label="Factor")
    dropdown = mo.ui.dropdown(
        options=["small", "medium", "large"],
        value="medium",
        label="Size:",
    )
    return slider, dropdown

@app.cell
def _cell_2(dropdown, slider):
    result = slider.value * 2
    return mo.md(f"""
        **selection:** {dropdown.value}

        **result:** {result}
        """
    ),