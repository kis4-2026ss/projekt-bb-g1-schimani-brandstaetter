import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    return mo,


@app.cell
def _cell_1(mo):
    mo.md(r"""# Widgets: slider, dropdown, and dependent output""")
    return


@app.cell
def _cell_2(mo):
    slider = mo.ui.slider(start=1, stop=10, value=3, label="Factor")
    dropdown = mo.ui.dropdown(
        options=["small", "medium", "large"],
        value="medium",
        label="Size:",
    )
    mo.vstack([slider, dropdown])
    return dropdown, slider


@app.cell
def _cell_3(dropdown, slider):
    result = slider.value * 2
    print("selection:", dropdown.value)
    print("result:", result)
    return result,


if __name__ == "__main__":
    app.run()