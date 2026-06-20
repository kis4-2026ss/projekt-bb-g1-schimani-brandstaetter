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

    df = pd.DataFrame({"city": ["Vienna", "Graz"], "value": [10, 20]})
    return df,


if __name__ == "__main__":
    app.run()