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
    # Small demo notebook

    Small example with Markdown, DataFrame display, HTML display, and a plot magic.
    """)
    return


@app.cell
def _cell_2():
    return


@app.cell
def _cell_3(mo):
    import pandas as pd
    import matplotlib.pyplot as plt

    values = pd.DataFrame(
        {
            "day": ["Mon", "Tue", "Wed", "Thu"],
            "orders": [12, 18, 15, 22],
        }
    )

    _total_orders_html = mo.Html(
        "<p><b>Total orders:</b> {}</p>".format(values["orders"].sum())
    )
    mo.vstack([values, _total_orders_html])
    return plt, values


@app.cell
def _cell_4(plt, values):
    _fig, _ax = plt.subplots()
    values.plot(
        x="day",
        y="orders",
        kind="bar",
        legend=False,
        title="Orders by day",
        ax=_ax,
    )
    _ax.set_ylabel("orders")
    _fig
    return


if __name__ == "__main__":
    app.run()
