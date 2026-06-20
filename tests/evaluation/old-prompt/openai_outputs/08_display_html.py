import marimo as mo
app = mo.App()

@app.cell
def _cell_0():
    return 

@app.cell
def _cell_1():
    from IPython.display import display, HTML
    display(HTML("<h3>Report</h3><p><b>Hello</b> from generated HTML.</p>"))
    return