import marimo

__generated_with = "0.23.10"
app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo

    return (mo,)


@app.cell
def _cell_1(mo):
    mo.md(r"""
    # Medium demo notebook

    Medium example with generated files, shell commands, captured shell output, CSV loading, timing, and a plot.
    """)
    return


@app.cell
def _cell_2():
    import os as _os

    _os.chdir(".")
    working_dir_set = True
    return


@app.cell
def _cell_3():
    with open("medium_notes.txt", "w", encoding="utf-8") as _f:
        _f.write(
            """Medium demo notes
    =================
    This file was generated from a Jupyter writefile magic.
    """
        )

    medium_notes_written = True
    return


@app.cell
def _cell_4():
    from pathlib import Path
    import pandas as pd
    import matplotlib.pyplot as plt

    _rows = []
    for _index in range(12):
        _rows.append(
            {
                "month": _index + 1,
                "revenue": 100 + _index * 12,
                "cost": 55 + _index * 7,
            }
        )

    df = pd.DataFrame(_rows)
    df["profit"] = df["revenue"] - df["cost"]
    df.to_csv("medium_sales.csv", index=False)

    path = None
    medium_sales_written = True
    return Path, pd


@app.cell
def _cell_5(mo):
    mo.md(r"""
    ## Inspect generated files
    """)
    return


@app.cell
def _cell_6(Path):
    generated_files = sorted(_path.name for _path in Path(".").iterdir())
    print(generated_files)
    return


@app.cell
def _cell_7(Path):
    print(Path("medium_notes.txt").read_text(encoding="utf-8"))
    return


@app.cell
def _cell_8(Path):
    csv_files = sorted(_path.name for _path in Path(".").glob("*.csv"))
    print("csv files:", csv_files)
    return


@app.cell
def _cell_9(pd):
    import time as _time

    _start_time = _time.perf_counter()

    loaded = pd.read_csv("medium_sales.csv")
    summary = loaded[["revenue", "cost", "profit"]].sum()
    print(summary)

    _end_time = _time.perf_counter()
    print(f"Wall time: {_end_time - _start_time:.6f} s")
    return (loaded,)


@app.cell
def _cell_10(loaded):
    ax = loaded.plot(
        x="month",
        y=["revenue", "cost", "profit"],
        marker="o",
        title="Monthly sales",
    )
    ax.set_ylabel("amount")
    _fig = ax.get_figure()
    _fig
    return


if __name__ == "__main__":
    app.run()
