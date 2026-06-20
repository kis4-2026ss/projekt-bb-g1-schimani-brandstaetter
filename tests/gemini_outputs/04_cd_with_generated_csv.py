import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md("# Working directory magic with generated CSV")


@app.cell
def _cell_1():
    import pandas as pd
    df = pd.DataFrame({"name": ["Ada", "Grace"], "score": [95, 98]})
    df.to_csv("scores.csv", index=False)
    return pd,


@app.cell
def _cell_2():
    import os
    os.chdir('.')
    return


@app.cell
def _cell_3(pd):
    loaded = pd.read_csv("scores.csv")
    print(loaded)
    return loaded,