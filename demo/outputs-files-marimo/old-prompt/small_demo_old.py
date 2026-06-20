import marimo

__generated_with = "0.23.10"
app = marimo.App()


@app.cell
def _cell_0(mo):
    # FEHLER 1:
    # `mo` wird als Zell-Parameter verwendet, aber in dieser Datei gibt es keine
    # vorherige Zelle, die `mo` zur Verfuegung stellt.
    # Korrektur aus small_demo_corrected.py:
    # @app.cell
    # def _cell_imports():
    #     import marimo as mo
    #     return mo,
    #
    # Danach darf diese Zelle `def _cell_0(mo):` verwenden.
    #
    mo.md(r"""
    # Small demo notebook

    Small example with Markdown, DataFrame display, HTML display, and a plot magic.
    """)
    return


@app.cell
def _cell_1():
    # FEHLER 3:
    # Die urspruengliche `%matplotlib inline`-Zelle wurde zu einer leeren
    # Zelle normalisiert. In small_demo_corrected.py wurde die Magic wenigstens
    # als get_ipython()-Fallback erhalten.
    # Korrektur aus small_demo_corrected.py:
    # try:
    #     from IPython import get_ipython
    #     _ipython = get_ipython()
    # except ImportError:
    #     _ipython = None
    #
    # if _ipython is not None:
    #     _ipython.run_line_magic("matplotlib", "inline")
    return


@app.cell
def _cell_2(mo):
    # FEHLER 1:
    # Auch diese Zelle braucht `mo`, aber `mo` wird in small_demo.py nirgends
    # als Zell-Output erzeugt. Siehe Korrektur mit `_cell_imports` oben.
    import pandas as _pd
    import matplotlib.pyplot as plt

    values = _pd.DataFrame(
        {
            "day": ["Mon", "Tue", "Wed", "Thu"],
            "orders": [12, 18, 15, 22],
        }
    )

    _total_orders = values["orders"].sum()
    # FEHLER 4:
    # Die sichtbare Ausgabe wird erzeugt, aber nicht returned.
    # Dadurch zeigt Marimo die Tabelle/HTML-Zusammenfassung nicht sicher an.
    # Korrektur aus small_demo_corrected.py:
    # return mo.vstack(
    #     [
    #         values,
    #         mo.Html(
    #             "<p><b>Total orders:</b> {}".format(values["orders"].sum())
    #         ),
    #     ]
    # ), plt, values
    mo.vstack(
        [
            values,
            mo.Html(f"<p><b>Total orders:</b> {_total_orders}</p>"),
        ]
    )
    return plt, values


@app.cell
def _cell_3(plt, values):
    _ax = values.plot(
        x="day",
        y="orders",
        kind="bar",
        legend=False,
        title="Orders by day",
    )
    _ax.set_ylabel("orders")
    plt.show()
    return


if __name__ == "__main__":
    app.run()
