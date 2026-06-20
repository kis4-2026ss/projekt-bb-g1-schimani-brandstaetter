import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    return mo,


@app.cell
def _cell_1(mo):
    mo.md(r"""# HTML display""")
    return


@app.cell
def _cell_2(mo):
    mo.Html("<h3>Report</h3><p><b>Hello</b> from generated HTML.</p>")
    return


if __name__ == "__main__":
    app.run()