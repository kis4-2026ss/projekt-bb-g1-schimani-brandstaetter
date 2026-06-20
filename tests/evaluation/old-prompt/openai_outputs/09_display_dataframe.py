import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return 

@app.cell
def _cell_1():
    import pandas as pd
    from IPython.display import display

    df = pd.DataFrame({"city": ["Vienna", "Graz"], "value": [10, 20]})
    display(df)
    return df, display, pd,