import marimo as mo

app = mo.App()


@app.cell
def _cell_0():
    mo.md(
        r"""
        # Medium demo notebook

        Medium example with generated files, shell commands, captured shell output, CSV loading, timing, and a plot.
        """
    )
    return


@app.cell
def _cell_1():
    import os as _os

    _os.chdir(".")
    return


@app.cell
def _cell_2(Path):
    # FEHLER 2:
    # `Path` wird hier als Zell-Parameter verlangt, bevor es von einer
    # vorherigen Zelle bereitgestellt wird. In Marimo ist diese Dependency kaputt.
    # Korrektur:
    # @app.cell
    # def _cell_2():
    #     from pathlib import Path
    #     Path("medium_notes.txt").write_text(
    #         """Medium demo notes
    # =================
    # This file was generated from a Jupyter writefile magic.
    # """
    #     )
    #     return Path,
    Path("medium_notes.txt").write_text(
        """Medium demo notes
=================
This file was generated from a Jupyter writefile magic.
"""
    )
    return


@app.cell
def _cell_3():
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

    _df = pd.DataFrame(_rows)
    _df["profit"] = _df["revenue"] - _df["cost"]
    _df.to_csv("medium_sales.csv", index=False)

    return Path, pd, plt


@app.cell
def _cell_4():
    mo.md(r"""## Inspect generated files""")
    return


@app.cell
def _cell_5(Path):
    _generated_files = sorted(_path.name for _path in Path(".").iterdir())
    print(_generated_files)
    return


@app.cell
def _cell_6(Path):
    print(Path("medium_notes.txt").read_text(encoding="utf-8"))
    return


@app.cell
def _cell_7(Path):
    _csv_files = sorted(_path.name for _path in Path(".").glob("*.csv"))
    print("csv files:", _csv_files)
    return


@app.cell
def _cell_8(pd):
    import time as _time

    _start_cpu = _time.process_time()
    _start_wall = _time.perf_counter()

    loaded = pd.read_csv("medium_sales.csv")
    _summary = loaded[["revenue", "cost", "profit"]].sum()
    print(_summary)

    _end_cpu = _time.process_time()
    _end_wall = _time.perf_counter()

    print(f"CPU times: total: {_end_cpu - _start_cpu:.3f} s")
    print(f"Wall time: {_end_wall - _start_wall:.3f} s")

    return loaded,


@app.cell
def _cell_9(loaded, plt):
    _ax = loaded.plot(
        x="month",
        y=["revenue", "cost", "profit"],
        marker="o",
        title="Monthly sales",
    )
    _ax.set_ylabel("amount")
    plt.show()
    return


if __name__ == "__main__":
    app.run()
