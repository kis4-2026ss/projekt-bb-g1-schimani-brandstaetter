import marimo

__generated_with = "0.23.10"
app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo

    mo.md(
        r"""
        # Large demo notebook

        Larger integrated demo with generated data, writefile magic, shell commands, captured output, widgets, HTML display, timing, tables, and plots.
        """
    )
    return (mo,)


@app.cell
def _cell_1():
    matplotlib_inline_enabled = True
    return


@app.cell
def _cell_2():
    import os

    os.chdir(".")
    cwd_set = True
    return


@app.cell
def _cell_3(mo):
    mo.md(r"""
    ## Imports and configuration
    """)
    return


@app.cell
def _cell_4():
    from pathlib import Path
    import pandas as pd
    import matplotlib.pyplot as plt

    report_title = "Operations Demo Report"
    data_file = "large_demo_data.csv"
    notes_file = "large_demo_notes.txt"
    regions = ["north", "south", "east", "west"]
    products = ["alpha", "beta", "gamma"]
    return (
        Path,
        data_file,
        notes_file,
        pd,
        plt,
        products,
        regions,
        report_title,
    )


@app.cell
def _cell_5(notes_file):
    with open(notes_file, "w", encoding="utf-8") as _file:
        _file.write(
            """Large demo notes
    ================
    This text file was created by a Jupyter cell magic.
    """
        )

    notes_file_written = True
    return


@app.cell
def _cell_6(mo):
    mo.md(r"""
    ## Generate synthetic operations data
    """)
    return


@app.cell
def _cell_7(data_file, pd, products, regions):
    _rows = []
    for _index in range(90):
        _region = regions[_index % len(regions)]
        _product = products[_index % len(products)]
        _units = 20 + (_index * 5) % 60
        _revenue = _units * (8 + _index % 5)
        _cost = _units * (4 + _index % 3)
        _rows.append(
            {
                "id": _index + 1,
                "region": _region,
                "product": _product,
                "units": _units,
                "revenue": _revenue,
                "cost": _cost,
            }
        )

    _raw = pd.DataFrame(_rows)
    _raw["profit"] = _raw["revenue"] - _raw["cost"]
    _raw.to_csv(data_file, index=False)

    _raw.head()
    data_file_written = True
    return


@app.cell
def _cell_8(mo):
    mo.md(r"""
    ## Inspect generated files
    """)
    return


@app.cell
def _cell_9(Path):
    _generated_files = sorted(_path.name for _path in Path(".").iterdir())
    print(_generated_files)
    return


@app.cell
def _cell_10(Path, notes_file):
    print(Path(notes_file).read_text(encoding="utf-8"))
    return


@app.cell
def _cell_11(Path):
    _csv_files = sorted(_path.name for _path in Path(".").glob("*.csv"))
    print("csv files:", _csv_files)
    return


@app.cell
def _cell_12(mo):
    mo.md(r"""
    ## Load and filter
    """)
    return


@app.cell
def _cell_13(Path, data_file, notes_file, pd):
    data = pd.read_csv(data_file)
    _notes = Path(notes_file).read_text(encoding="utf-8")
    print(_notes)

    data.head(8)
    return (data,)


@app.cell
def _cell_14(data, mo):
    region_widget = mo.ui.dropdown(
        options=["all"] + sorted(data["region"].unique()),
        value="all",
        label="Region:",
    )
    min_profit_widget = mo.ui.slider(
        start=0,
        stop=500,
        step=25,
        value=100,
        label="Min profit:",
    )

    mo.vstack([region_widget, min_profit_widget])
    return min_profit_widget, region_widget


@app.cell
def _cell_15(data, min_profit_widget, region_widget):
    filtered = data[data["profit"] >= min_profit_widget.value]
    if region_widget.value != "all":
        filtered = filtered[filtered["region"] == region_widget.value]

    summary = filtered.groupby("product")[["units", "revenue", "cost", "profit"]].mean()

    summary
    return filtered, summary


@app.cell
def _cell_16(filtered):
    import timeit

    _timer = timeit.Timer(lambda: filtered["profit"].sum())
    _loops, _ = _timer.autorange()
    _times = _timer.repeat(repeat=7, number=_loops)
    _best = min(_times) / _loops
    print(f"{_best:.6g} seconds per loop (best of 7 runs, {_loops} loops each)")

    benchmark_done = True
    return


@app.cell
def _cell_17(filtered):
    import time

    _start_cpu_time = time.process_time()
    _start_wall_time = time.perf_counter()

    try:
        total_revenue = filtered["revenue"].sum()
        total_profit = filtered["profit"].sum()
        print("total revenue:", total_revenue)
        print("total profit:", total_profit)
    finally:
        _end_cpu_time = time.process_time()
        _end_wall_time = time.perf_counter()
        print(f"CPU times: total: {_end_cpu_time - _start_cpu_time:.3f} s")
        print(f"Wall time: {_end_wall_time - _start_wall_time:.3f} s")
    return total_profit, total_revenue


@app.cell
def _cell_18(mo):
    mo.md(r"""
    ## Rich report
    """)
    return


@app.cell
def _cell_19(filtered, mo, report_title, total_profit, total_revenue):
    mo.Html(
        f"<h2>{report_title}</h2>"
        f"<p>Rows after filtering: <b>{len(filtered)}</b></p>"
        f"<p>Total revenue: <b>{total_revenue}</b></p>"
        f"<p>Total profit: <b>{total_profit}</b></p>"
    )
    return


@app.cell
def _cell_20(summary):
    _ax = summary["profit"].plot(kind="bar", title="Average profit by product")
    _ax.set_ylabel("profit")
    _fig = _ax.get_figure()
    _fig.tight_layout()

    _fig
    avg_profit_plot_done = True
    return


@app.cell
def _cell_21(filtered, plt):
    _fig, _ax = plt.subplots()
    _ax.scatter(filtered["revenue"], filtered["profit"], alpha=0.7)
    _ax.set_xlabel("revenue")
    _ax.set_ylabel("profit")
    _ax.set_title("Revenue vs profit")
    _fig.tight_layout()

    _fig
    return


if __name__ == "__main__":
    app.run()
