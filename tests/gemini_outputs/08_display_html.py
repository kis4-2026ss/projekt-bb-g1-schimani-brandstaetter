import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md("# HTML display"),


@app.cell
def _cell_1():
    _html_content = "<h3>Report</h3><p><b>Hello</b> from generated HTML.</p>"
    return mo.md(_html_content),