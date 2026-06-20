import marimo as mo

app = mo.App()


@app.cell
def _cell_0():
    mo.md(
        r"""
        # Large demo notebook

        Larger integrated demo with generated data, writefile magic, shell commands, captured output, widgets, HTML display, timing, tables, and plots.
        """
    )
    return


@app.cell
def _cell_1():
    try:
        _ipython = get_ipython()
    except NameError:
        _ipython = None

    if _ipython is not None:
        _ipython.run_line_magic("matplotlib", "inline")
    return


@app.cell
def _cell_2():
    import os

    os.chdir(".")
    return


@app.cell
def _cell_3():
    mo.md(r"""## Imports and configuration""")
    return


@app.cell
def _cell_4():
    from pathlib import Path
    import pandas as pd
    import matplotlib.pyplot as plt
    import ipywidgets as widgets
    from IPython.display import display, HTML

    report_title = "Operations Demo Report"
    data_file = "large_demo_data.csv"
    notes_file = "large_demo_notes.txt"
    regions = ["north", "south", "east", "west"]
    products = ["alpha", "beta", "gamma"]

    return (
        HTML,
        Path,
        data_file,
        display,
        notes_file,
        pd,
        plt,
        products,
        regions,
        report_title,
        widgets,
    )


@app.cell
def _cell_5(Path, notes_file):
    Path(notes_file).write_text(
        """Large demo notes
================
This text file was created by a Jupyter cell magic.
"""
    )
    notes_written = True
    return notes_written,


@app.cell
def _cell_6():
    mo.md(r"""## Generate synthetic operations data""")
    return


@app.cell
def _cell_7(data_file, display, pd, products, regions):
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
    # FEHLER 2:
    # `display(...)` aus IPython ist keine saubere Marimo-Ausgabe.
    # Korrektur:
    # return data_written, _raw.head()
    display(_raw.head())

    data_written = True
    return data_written,


@app.cell
def _cell_8():
    mo.md(r"""## Inspect generated files""")
    return


@app.cell
def _cell_9(Path, data_written, notes_written):
    _ = (data_written, notes_written)
    generated_files = sorted(_path.name for _path in Path(".").iterdir())
    print(generated_files)
    return


@app.cell
def _cell_10(Path, notes_file, notes_written):
    _ = notes_written
    print(Path(notes_file).read_text(encoding="utf-8"))
    return


@app.cell
def _cell_11(Path, data_written):
    _ = data_written
    csv_files = sorted(_path.name for _path in Path(".").glob("*.csv"))
    print("csv files:", csv_files)
    return


@app.cell
def _cell_12():
    mo.md(r"""## Load and filter""")
    return


@app.cell
def _cell_13(
    Path,
    data_file,
    data_written,
    display,
    notes_file,
    notes_written,
    pd,
):
    _ = (data_written, notes_written)
    data = pd.read_csv(data_file)
    _notes = Path(notes_file).read_text(encoding="utf-8")
    print(_notes)
    # FEHLER 2:
    # `display(...)` aus IPython ist keine saubere Marimo-Ausgabe.
    # Korrektur:
    # return data, data.head(8)
    display(data.head(8))
    return data,


@app.cell
def _cell_14(data, display, widgets):
    _ = (display, widgets)

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

    # FEHLER 3:
    # Die Widget-Ausgabe wird erzeugt, aber nicht zurueckgegeben.
    # Dadurch koennen die Controls in Marimo unsichtbar bleiben.
    # Korrektur:
    # return min_profit_widget, region_widget, mo.vstack([region_widget, min_profit_widget])
    mo.vstack([region_widget, min_profit_widget])
    return min_profit_widget, region_widget


@app.cell
def _cell_15(data, display, min_profit_widget, region_widget):
    filtered = data[data["profit"] >= min_profit_widget.value]
    if region_widget.value != "all":
        filtered = filtered[filtered["region"] == region_widget.value]

    summary = filtered.groupby("product")[["units", "revenue", "cost", "profit"]].mean()
    # FEHLER 2:
    # `display(...)` aus IPython ist keine saubere Marimo-Ausgabe.
    # Korrektur:
    # return filtered, summary
    display(summary)

    return filtered, summary


@app.cell
def _cell_16(filtered):
    import timeit

    _timer = timeit.Timer(lambda: filtered["profit"].sum())
    _loops, _discard = _timer.autorange()
    _results = _timer.repeat(repeat=7, number=_loops)
    _best = min(_results) / _loops
    print(f"{_best:.6g} seconds per loop (best of 7 runs, {_loops} loops each)")
    return


@app.cell
def _cell_17(filtered):
    import time

    _start_wall = time.perf_counter()
    _start_cpu = time.process_time()
    try:
        total_revenue = filtered["revenue"].sum()
        total_profit = filtered["profit"].sum()
        print("total revenue:", total_revenue)
        print("total profit:", total_profit)
    finally:
        _elapsed_wall = time.perf_counter() - _start_wall
        _elapsed_cpu = time.process_time() - _start_cpu
        print(f"CPU times: total: {_elapsed_cpu:.6g} s")
        print(f"Wall time: {_elapsed_wall:.6g} s")

    return total_profit, total_revenue


@app.cell
def _cell_18():
    mo.md(r"""## Rich report""")
    return


@app.cell
def _cell_19(
    HTML,
    display,
    filtered,
    report_title,
    total_profit,
    total_revenue,
):
    # FEHLER 4:
    # HTML wird ueber IPython `display(HTML(...))` ausgegeben.
    # In Marimo sollte das als Marimo-Objekt returned werden.
    # Korrektur:
    # return mo.Html(
    #     f"<h2>{report_title}</h2>"
    #     f"<p>Rows after filtering: <b>{len(filtered)}</b></p>"
    #     f"<p>Total revenue: <b>{total_revenue}</b></p>"
    #     f"<p>Total profit: <b>{total_profit}</b></p>"
    # )
    display(
        HTML(
            f"<h2>{report_title}</h2>"
            f"<p>Rows after filtering: <b>{len(filtered)}</b></p>"
            f"<p>Total revenue: <b>{total_revenue}</b></p>"
            f"<p>Total profit: <b>{total_profit}</b></p>"
        )
    )
    return


@app.cell
def _cell_20(plt, summary):
    _ax = summary["profit"].plot(kind="bar", title="Average profit by product")
    _ax.set_ylabel("profit")
    plt.show()
    return


@app.cell
def _cell_21(filtered, plt):
    _fig, _ax = plt.subplots()
    _ax.scatter(filtered["revenue"], filtered["profit"], alpha=0.7)
    _ax.set_xlabel("revenue")
    _ax.set_ylabel("profit")
    _ax.set_title("Revenue vs profit")
    plt.show()
    return


if __name__ == "__main__":
    app.run()
