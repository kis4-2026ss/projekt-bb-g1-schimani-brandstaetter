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
    # Combined Jupyter feature report

    This notebook intentionally combines several Jupyter-specific
    features in one larger workflow: magics, shell commands, generated
    files, captured shell output, widgets, rich display, timing, and
    plots.
    """)
    return


@app.cell
def _cell_2():
    return


@app.cell
def _cell_3():
    import os as _os

    _os.chdir(".")
    cwd_set = True
    return


@app.cell
def _cell_4(mo):
    mo.md(r"""
    ## Imports and report configuration

    The next cell defines reusable report settings and imports the
    libraries used throughout the notebook.
    """)
    return


@app.cell
def _cell_5():
    from pathlib import Path
    import pandas as pd
    import matplotlib.pyplot as plt

    report_title = "Synthetic Operations Report"
    filename = "report_data.csv"
    notes_file = "report_notes.txt"
    categories = ["alpha", "beta", "gamma", "delta"]
    regions = ["north", "south", "east", "west"]
    return (
        Path,
        categories,
        filename,
        notes_file,
        pd,
        plt,
        regions,
        report_title,
    )


@app.cell
def _cell_6(mo):
    mo.md(r"""
    ## Generate report notes

    The next cell writes a small text file with Jupyter's writefile
    magic.
    """)
    return


@app.cell
def _cell_7(notes_file):
    with open(notes_file, "w", encoding="utf-8") as _f:
        _f.write(
            """Generated report notes
    ======================
    This file was written from a Jupyter cell.
    """
        )

    notes_written = True
    return


@app.cell
def _cell_8(mo):
    mo.md(r"""
    ## Create synthetic report data

    The CSV file is generated inside the notebook. No external input file
    is required.
    """)
    return


@app.cell
def _cell_9(categories, filename, pd, regions):
    _rows = []
    for _index in range(120):
        _category = categories[_index % len(categories)]
        _region = regions[_index % len(regions)]
        _value = 20 + (_index * 9) % 75
        _cost = 8 + (_index * 4) % 35
        _rows.append(
            {
                "id": _index + 1,
                "category": _category,
                "region": _region,
                "value": _value,
                "cost": _cost,
            }
        )

    _raw_data = pd.DataFrame(_rows)
    _raw_data["profit"] = _raw_data["value"] - _raw_data["cost"]
    _raw_data.to_csv(filename, index=False)

    _raw_data.head()
    csv_written = True
    return


@app.cell
def _cell_10(mo):
    mo.md(r"""
    ## Inspect generated files with shell commands

    These cells intentionally use Jupyter shell syntax and captured shell
    output.
    """)
    return


@app.cell
def _cell_11():
    import subprocess

    subprocess.run(["ls"], check=False)
    ls_completed = True
    return (subprocess,)


@app.cell
def _cell_12(filename, subprocess):
    subprocess.run(f"cat {filename}", shell=True)
    cat_completed = True
    return


@app.cell
def _cell_13(subprocess):
    _result = subprocess.run(
        "ls *.csv",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    files = _result.stdout.splitlines()
    print("csv files:", files)
    return


@app.cell
def _cell_14(mo):
    mo.md(r"""
    ## Read files back into Python

    The generated CSV and text note are loaded again for the report.
    """)
    return


@app.cell
def _cell_15(Path, filename, notes_file, pd):
    data = pd.read_csv(filename)
    notes = Path(notes_file).read_text(encoding="utf-8")
    print(notes)

    data.head(10)
    return (data,)


@app.cell
def _cell_16(mo):
    mo.md(r"""
    ## Interactive filters

    These widgets control which rows are included in the summary.
    """)
    return


@app.cell
def _cell_17(data, mo):
    region_widget = mo.ui.dropdown(
        options=["all"] + sorted(data["region"].unique()),
        value="all",
        label="Region:",
    )
    min_profit_widget = mo.ui.slider(
        start=0,
        stop=80,
        step=5,
        value=10,
        label="Min profit:",
        show_value=True,
    )

    mo.vstack([region_widget, min_profit_widget])
    return min_profit_widget, region_widget


@app.cell
def _cell_18(mo):
    mo.md(r"""
    ## Filter and summarize data

    The filtered result depends on both widget values.
    """)
    return


@app.cell
def _cell_19(data, min_profit_widget, region_widget):
    filtered = data[data["profit"] >= min_profit_widget.value]
    if region_widget.value != "all":
        filtered = filtered[filtered["region"] == region_widget.value]

    summary = filtered.groupby("category")[["value", "cost", "profit"]].mean()

    summary
    return filtered, summary


@app.cell
def _cell_20(data):
    import timeit as _timeit

    _timer = _timeit.Timer(lambda: data["value"].sum())
    _loops, _ = _timer.autorange()
    _repeats = _timer.repeat(repeat=7, number=_loops)
    _best = min(_repeats) / _loops
    print(f"{_best:.6g} s per loop (best of 7, {_loops} loops each)")
    return


@app.cell
def _cell_21(mo):
    mo.md(r"""
    ## Timed report calculation

    This cell uses a cell magic around a small aggregate calculation.
    """)
    return


@app.cell
def _cell_22(filtered):
    import os as _os
    import time as _time

    def _format_time_interval(seconds):
        _abs_seconds = abs(seconds)
        if _abs_seconds >= 1:
            return f"{seconds:.3g} s"
        if _abs_seconds >= 1e-3:
            return f"{seconds * 1e3:.3g} ms"
        if _abs_seconds >= 1e-6:
            return f"{seconds * 1e6:.3g} µs"
        return f"{seconds * 1e9:.3g} ns"

    _start_times = _os.times()
    _start_wall = _time.perf_counter()
    try:
        total_value = filtered["value"].sum()
        total_profit = filtered["profit"].sum()
        print("total value:", total_value)
        print("total profit:", total_profit)
    finally:
        _end_wall = _time.perf_counter()
        _end_times = _os.times()
        _user_time = _end_times.user - _start_times.user
        _sys_time = _end_times.system - _start_times.system
        _total_cpu_time = _user_time + _sys_time
        _wall_time = _end_wall - _start_wall
        print(
            f"CPU times: user {_format_time_interval(_user_time)}, "
            f"sys: {_format_time_interval(_sys_time)}, "
            f"total: {_format_time_interval(_total_cpu_time)}"
        )
        print(f"Wall time: {_format_time_interval(_wall_time)}")
    return total_profit, total_value


@app.cell
def _cell_23(mo):
    mo.md(r"""
    ## Rich HTML report

    The report combines values computed in earlier cells.
    """)
    return


@app.cell
def _cell_24(filtered, mo, report_title, total_profit, total_value):
    mo.Html(
        f"<h2>{report_title}</h2>"
        f"<p>Rows after filtering: <b>{len(filtered)}</b></p>"
        f"<p>Total value: <b>{total_value}</b></p>"
        f"<p>Total profit: <b>{total_profit}</b></p>"
    )
    return


@app.cell
def _cell_25(mo):
    mo.md(r"""
    ## Plot results

    The final charts should make the category-level differences visible.
    """)
    return


@app.cell
def _cell_26(summary):
    _ax = summary["profit"].plot(kind="bar", title="Average profit by category")
    _ax.set_ylabel("profit")
    _ax.figure
    return


@app.cell
def _cell_27(filtered, plt):
    _fig, _ax = plt.subplots()
    _ax.scatter(filtered["value"], filtered["profit"], alpha=0.7)
    _ax.set_xlabel("value")
    _ax.set_ylabel("profit")
    _ax.set_title("Value vs profit")
    _fig
    return


if __name__ == "__main__":
    app.run()
