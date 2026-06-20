import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    return mo,


@app.cell
def _cell_1(mo):
    mo.md(r"""# Working directory magic with generated CSV""")
    return


@app.cell
def _cell_2():
    import pandas as pd

    df = pd.DataFrame({"name": ["Ada", "Grace"], "score": [95, 98]})
    df.to_csv("scores.csv", index=False)
    file_written = True
    return df, file_written, pd


@app.cell
def _cell_3(file_written):
    import os

    os.chdir(".")
    print(os.getcwd())
    working_directory_set = True
    return os, working_directory_set


@app.cell
def _cell_4(file_written, pd, working_directory_set):
    loaded = pd.read_csv("scores.csv")
    print(loaded)
    return loaded,


if __name__ == "__main__":
    app.run()