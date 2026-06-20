import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    import pandas as pd

    return mo, pd


@app.cell
def _cell_1(mo):
    mo.md("# DataFrame display")
    return


@app.cell
def _cell_2(pd):
    df = pd.DataFrame({"city": ["Vienna", "Graz"], "value": [10, 20]})
    df
    return df,


if __name__ == "__main__":
    app.run()