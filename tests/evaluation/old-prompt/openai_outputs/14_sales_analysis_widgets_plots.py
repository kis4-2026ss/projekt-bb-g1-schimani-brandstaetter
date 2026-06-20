import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# Explorative sales analysis\n\nThis larger notebook creates synthetic sales data, filters it with widgets, and shows grouped tables and plots."),


@app.cell
def _cell_1(plt):
    plt.ion()
    return plt,


@app.cell
def _cell_2(plt):
    import pandas as pd
    import ipywidgets as widgets
    from IPython.display import display

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
    display(sales.head())
    return display, sales, widgets,


@app.cell
def _cell_3():
    return mo.md("## Interactive filter setup\n\nThe next cells create controls for selecting a region and a minimum revenue. The filtered data should update the summary used for the chart."),


@app.cell
def _cell_4(display, sales, widgets):
    region_dropdown = widgets.Dropdown(
        options=["all"] + sorted(sales["region"].unique()),
        value="all",
        description="Region:",
    )
    min_revenue = widgets.IntSlider(
        value=120,
        min=80,
        max=180,
        step=10,
        description="Min rev:",
    )

    display(region_dropdown)
    display(min_revenue)
    return min_revenue, region_dropdown,


@app.cell
def _cell_5():
    return mo.md("## Aggregated sales summary\n\nThis step groups the filtered rows by category and compares average revenue with average profit."),


@app.cell
def _cell_6(display, sales, min_revenue, region_dropdown):
    filtered = sales[sales["revenue"] >= min_revenue.value]
    if region_dropdown.value != "all":
        filtered = filtered[filtered["region"] == region_dropdown.value]

    summary = filtered.groupby("category")[["revenue", "profit"]].mean()
    display(summary)
    return summary,


@app.cell
def _cell_7():
    return mo.md("## Profit chart\n\nThe final chart should make it easy to compare which category has the highest average profit after filtering."),


@app.cell
def _cell_8(plt, summary):
    import time

    start_time = time.time()
    ax = summary["profit"].plot(kind="bar", title="Average profit by category")
    ax.set_ylabel("profit")
    plt.show()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")
    return