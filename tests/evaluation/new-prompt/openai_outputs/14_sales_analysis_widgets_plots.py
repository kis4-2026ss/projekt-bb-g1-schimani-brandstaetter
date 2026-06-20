import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    return mo,


@app.cell
def _cell_1(mo):
    mo.md(
        r"""
        # Explorative sales analysis

        This larger notebook creates synthetic sales data, filters it with
        widgets, and shows grouped tables and plots.
        """
    )
    return


@app.cell
def _cell_2():
    return


@app.cell
def _cell_3():
    import pandas as pd
    import matplotlib.pyplot as plt

    _dates = pd.date_range("2026-01-01", periods=60, freq="D")
    _regions = ["north", "south", "east", "west"]
    _categories = ["hardware", "software", "service"]

    _rows = []
    for _index, _date in enumerate(_dates):
        _region = _regions[_index % len(_regions)]
        _category = _categories[_index % len(_categories)]
        _revenue = 100 + (_index * 7) % 80
        _cost = 45 + (_index * 5) % 40
        _rows.append(
            {
                "date": _date,
                "region": _region,
                "category": _category,
                "revenue": _revenue,
                "cost": _cost,
            }
        )

    sales = pd.DataFrame(_rows)
    sales["profit"] = sales["revenue"] - sales["cost"]

    _sales_preview = sales.head()
    _sales_preview

    display = None
    widgets = None
    return display, plt, sales, widgets


@app.cell
def _cell_4(mo):
    mo.md(
        r"""
        ## Interactive filter setup

        The next cells create controls for selecting a region and a minimum
        revenue. The filtered data should update the summary used for the
        chart.
        """
    )
    return


@app.cell
def _cell_5(display, mo, sales, widgets):
    _ = (display, widgets)

    region_dropdown = mo.ui.dropdown(
        options=["all"] + sorted(sales["region"].unique()),
        value="all",
        label="Region:",
    )
    min_revenue = mo.ui.slider(
        start=80,
        stop=180,
        step=10,
        value=120,
        label="Min rev:",
    )

    mo.vstack([region_dropdown, min_revenue])
    return min_revenue, region_dropdown


@app.cell
def _cell_6(mo):
    mo.md(
        r"""
        ## Aggregated sales summary

        This step groups the filtered rows by category and compares average
        revenue with average profit.
        """
    )
    return


@app.cell
def _cell_7(display, min_revenue, region_dropdown, sales):
    _ = display

    filtered = sales[sales["revenue"] >= min_revenue.value]
    if region_dropdown.value != "all":
        filtered = filtered[filtered["region"] == region_dropdown.value]

    summary = filtered.groupby("category")[["revenue", "profit"]].mean()
    summary

    return filtered, summary


@app.cell
def _cell_8(mo):
    mo.md(
        r"""
        ## Profit chart

        The final chart should make it easy to compare which category has the
        highest average profit after filtering.
        """
    )
    return


@app.cell
def _cell_9(plt, summary):
    import time as _time

    _start_cpu = _time.process_time()
    _start_wall = _time.perf_counter()

    _figure, _ax = plt.subplots()
    summary["profit"].plot(kind="bar", title="Average profit by category", ax=_ax)
    _ax.set_ylabel("profit")

    _end_cpu = _time.process_time()
    _end_wall = _time.perf_counter()

    print(f"CPU times: total {_end_cpu - _start_cpu:.6g} s")
    print(f"Wall time: {_end_wall - _start_wall:.6g} s")

    _figure
    return


if __name__ == "__main__":
    app.run()