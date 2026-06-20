import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md(
        """
        # Explorative sales analysis

        This larger notebook creates synthetic sales data, filters it with
        widgets, and shows grouped tables and plots.
        """
    )


@app.cell
def _cell_1():
    # Matplotlib display magic omitted for Marimo compatibility.
    return


@app.cell
def _cell_2():
    import pandas as pd
    import matplotlib.pyplot as plt

    dates = pd.date_range("2026-01-01", periods=60, freq="D")
    regions = ["north", "south", "east", "west"]
    categories = ["hardware", "software", "service"]

    rows = []
    for index, date in enumerate(dates):
        region = regions[index % len(regions)]
        category = categories[index % len(categories)]
        revenue = 100 + (index * 7) % 80
        cost = 45 + (index * 5) % 40
        rows.append({
            "date": date,
            "region": region,
            "category": category,
            "revenue": revenue,
            "cost": cost,
        })

    sales = pd.DataFrame(rows)
    sales["profit"] = sales["revenue"] - sales["cost"]
    # In Marimo, returning the DataFrame implicitly displays it,
    # or you can wrap it in mo.ui.dataframe(sales.head()) for explicit display.
    # For this exercise, we will return the full dataframe.
    return sales, plt,


@app.cell
def _cell_3():
    return mo.md(
        """
        ## Interactive filter setup

        The next cells create controls for selecting a region and a minimum
        revenue. The filtered data should update the summary used for the
        chart.
        """
    )


@app.cell
def _cell_4(sales):
    region_dropdown = mo.ui.Dropdown(
        options=["all"] + sorted(sales["region"].unique()),
        value="all",
        label="Region:",
    )
    min_revenue = mo.ui.IntSlider(
        value=120,
        min=80,
        max=180,
        step=10,
        label="Min rev:",
    )

    # In Marimo, mo.ui components are implicitly displayed if they are
    # the last expression or returned from the cell.
    return min_revenue, region_dropdown,


@app.cell
def _cell_5():
    return mo.md(
        """
        ## Aggregated sales summary

        This step groups the filtered rows by category and compares average
        revenue with average profit.
        """
    )


@app.cell
def _cell_6(min_revenue, region_dropdown, sales):
    filtered = sales[sales["revenue"] >= min_revenue.value]
    if region_dropdown.value != "all":
        filtered = filtered[filtered["region"] == region_dropdown.value]

    summary = filtered.groupby("category")[["revenue", "profit"]].mean()
    # In Marimo, returning the DataFrame implicitly displays it.
    return summary,


@app.cell
def _cell_7():
    return mo.md(
        """
        ## Profit chart

        The final chart should make it easy to compare which category has the
        highest average profit after filtering.
        """
    )


@app.cell
def _cell_8(plt, summary):
    # import matplotlib.pyplot as plt is not needed here as plt is passed
    # as a dependency from _cell_2
    _fig, ax = plt.subplots()  # Use _fig to avoid naming collision if fig were used
    summary["profit"].plot(kind="bar", title="Average profit by category", ax=ax)
    ax.set_ylabel("profit")
    # plt.show() is not needed in Marimo; returning the plot object displays it.
    return _fig, ax,