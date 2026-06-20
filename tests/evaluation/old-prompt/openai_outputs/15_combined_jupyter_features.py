import marimo as mo
app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# Combined Jupyter feature report\n\nThis notebook intentionally combines several Jupyter-specific\nfeatures in one larger workflow: magics, shell commands, generated\nfiles, captured shell output, widgets, rich display, timing, and\nplots."),

@app.cell
def _cell_1():
    get_ipython().run_line_magic("matplotlib", "inline")
    return 

@app.cell
def _cell_2():
    import os
    os.chdir('.')
    return os,

@app.cell
def _cell_3():
    return mo.md("## Imports and report configuration\n\nThe next cell defines reusable report settings and imports the\nlibraries used throughout the notebook."),

@app.cell
def _cell_4(os):
    from pathlib import Path
    import pandas as pd
    import matplotlib.pyplot as plt
    import ipywidgets as widgets
    from IPython.display import display, HTML

    report_title = "Synthetic Operations Report"
    filename = "report_data.csv"
    notes_file = "report_notes.txt"
    categories = ["alpha", "beta", "gamma", "delta"]
    regions = ["north", "south", "east", "west"]
    
    return report_title, filename, notes_file, categories, regions, display, pd, plt, widgets,

@app.cell
def _cell_5():
    return mo.md("## Generate report notes\n\nThe next cell writes a small text file with Jupyter's writefile magic."),

@app.cell
def _cell_6():
    with open('report_notes.txt', 'w') as f:
        f.write('Generated report notes\n')
        f.write('======================\n')
        f.write('This file was written from a Jupyter cell.\n')
    return f,

@app.cell
def _cell_7():
    return mo.md("## Create synthetic report data\n\nThe CSV file is generated inside the notebook. No external input file\nis required."),

@app.cell
def _cell_8(categories, regions, display, pd, filename):
    rows = []
    for index in range(120):
        category = categories[index % len(categories)]
        region = regions[index % len(regions)]
        value = 20 + (index * 9) % 75
        cost = 8 + (index * 4) % 35
        rows.append({
            "id": index + 1,
            "category": category,
            "region": region,
            "value": value,
            "cost": cost,
        })

    raw_data = pd.DataFrame(rows)
    raw_data["profit"] = raw_data["value"] - raw_data["cost"]
    raw_data.to_csv(filename, index=False)
    display(raw_data.head())
    return raw_data,

@app.cell
def _cell_9():
    return mo.md("## Inspect generated files with shell commands\n\nThese cells intentionally use Jupyter shell syntax and captured shell\noutput."),

@app.cell
def _cell_10(os):
    os.system('ls')
    return

@app.cell
def _cell_11(f):
    with open(f.name, 'r') as f:
        print(f.read())
    return 

@app.cell
def _cell_12():
    import glob
    files = glob.glob("*.csv")
    print("csv files:", files)
    return files,

@app.cell
def _cell_13():
    return mo.md("## Read files back into Python\n\nThe generated CSV and text note are loaded again for the report."),

@app.cell
def _cell_14(Path, display, filename, notes_file, pd):
    data = pd.read_csv(filename)
    notes = Path(notes_file).read_text(encoding="utf-8")
    print(notes)
    display(data.head(10))
    return data, notes,

@app.cell
def _cell_15():
    return mo.md("## Interactive filters\n\nThese widgets control which rows are included in the summary."),

@app.cell
def _cell_16(data, display, widgets):
    region_widget = widgets.Dropdown(
        options=["all"] + sorted(data["region"].unique()),
        value="all",
        description="Region:",
    )
    min_profit_widget = widgets.IntSlider(
        value=10,
        min=0,
        max=80,
        step=5,
        description="Min profit:",
    )

    display(region_widget)
    display(min_profit_widget)
    return region_widget, min_profit_widget,

@app.cell
def _cell_17():
    return mo.md("## Filter and summarize data\n\nThe filtered result depends on both widget values."),

@app.cell
def _cell_18(data, display, min_profit_widget, region_widget):
    filtered = data[data["profit"] >= min_profit_widget.value]
    if region_widget.value != "all":
        filtered = filtered[filtered["region"] == region_widget.value]

    summary = filtered.groupby("category")[["value", "cost", "profit"]].mean()
    display(summary)
    return filtered, summary,

@app.cell
def _cell_19():
    import timeit
    timeit.timeit('data["value"].sum()', globals=globals(), number=10000)
    return 

@app.cell
def _cell_20():
    return mo.md("## Timed report calculation\n\nThis cell uses a cell magic around a small aggregate calculation."),

@app.cell
def _cell_21(filtered):
    import time
    start_time = time.time()
    total_value = filtered["value"].sum()
    total_profit = filtered["profit"].sum()
    print("total value:", total_value)
    print("total profit:", total_profit)
    print("Execution time: %s seconds" % (time.time() - start_time))
    return total_value, total_profit,

@app.cell
def _cell_22():
    return mo.md("## Rich HTML report\n\nThe report combines values computed in earlier cells."),

@app.cell
def _cell_23(HTML, display, report_title, total_value, total_profit, filtered):
    display(HTML(
        f"<h2>{report_title}</h2>"
        f"<p>Rows after filtering: <b>{len(filtered)}</b></p>"
        f"<p>Total value: <b>{total_value}</b></p>"
        f"<p>Total profit: <b>{total_profit}</b></p>"
    ))
    return 

@app.cell
def _cell_24():
    return mo.md("## Plot results\n\nThe final charts should make the category-level differences visible."),

@app.cell
def _cell_25(summary, plt):
    ax = summary["profit"].plot(kind="bar", title="Average profit by category")
    ax.set_ylabel("profit")
    plt.show()
    return ax,

@app.cell
def _cell_26(ax, filtered, plt):
    fig, ax = plt.subplots()
    ax.scatter(filtered["value"], filtered["profit"], alpha=0.7)
    ax.set_xlabel("value")
    ax.set_ylabel("profit")
    ax.set_title("Value vs profit")
    plt.show()
    return fig, ax,