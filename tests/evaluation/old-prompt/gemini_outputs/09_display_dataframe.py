import marimo as mo
app = mo.App()

@app.cell
def _cell_0():
    return mo.md(
        """
        # DataFrame display
        """
    )

@app.cell
def _cell_1():
    import pandas as pd
    # The `IPython.display.display` function is not directly used in Marimo for
    # displaying DataFrames; Marimo automatically renders the DataFrame when it's
    # the last expression or returned from a cell.
    
    df = pd.DataFrame({"city": ["Vienna", "Graz"], "value": [10, 20]})
    return df, pd