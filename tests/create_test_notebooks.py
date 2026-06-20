from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent


OUTPUT_DIR = Path(__file__).parent / "test_notebooks"


def markdown(source: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": dedent(source).strip() + "\n",
    }


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": dedent(source).strip() + "\n",
    }


def notebook(cells: list[dict]) -> dict:
    return {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
                "pygments_lexer": "ipython3",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }


NOTEBOOKS: dict[str, list[dict]] = {
    "01_basic_python_imports_functions.ipynb": [
        markdown(
            """
            # Basic Python, imports, functions, and data flow

            This notebook checks ordinary Python dependencies before any
            Jupyter-specific syntax is introduced.
            """
        ),
        code(
            """
            import pandas as pd
            from pathlib import Path

            base = 10
            """
        ),
        code(
            """
            def add_tax(value):
                return value * 1.2
            """
        ),
        code(
            """
            df = pd.DataFrame({"value": [base, add_tax(base)]})
            current_path = Path(".")
            print(current_path.resolve())
            print(df)
            """
        ),
    ],
    "02_timing_magics.ipynb": [
        markdown("# Timing magics"),
        code("%timeit x = 10"),
        code(
            """
            %%time
            total = sum(range(100000))
            print(total)
            """
        ),
    ],
    "03_matplotlib_inline_plot.ipynb": [
        markdown("# Matplotlib inline plot"),
        code(
            """
            %matplotlib inline
            import matplotlib.pyplot as plt

            values = [1, 4, 9, 16]
            plt.plot(values, marker="o")
            plt.title("Square values")
            plt.show()
            """
        ),
    ],
    "04_cd_with_generated_csv.ipynb": [
        markdown("# Working directory magic with generated CSV"),
        code(
            """
            import pandas as pd

            df = pd.DataFrame({"name": ["Ada", "Grace"], "score": [95, 98]})
            df.to_csv("scores.csv", index=False)
            """
        ),
        code("%cd ."),
        code(
            """
            loaded = pd.read_csv("scores.csv")
            print(loaded)
            """
        ),
    ],
    "05_bash_cell_magic.ipynb": [
        markdown("# Bash cell magic"),
        code(
            """
            %%bash
            echo "hello from bash"
            ls
            """
        ),
    ],
    "06_writefile_magic.ipynb": [
        markdown("# Writefile magic"),
        code(
            """
            %%writefile hello.txt
            Hello from notebook
            """
        ),
        code(
            """
            with open("hello.txt", encoding="utf-8") as file:
                print(file.read())
            """
        ),
    ],
    "07_shell_commands_variables_capture.ipynb": [
        markdown("# Shell commands with variables and captured output"),
        code(
            """
            from pathlib import Path

            filename = "data.csv"
            Path(filename).write_text("a,b\\n1,2\\n", encoding="utf-8")
            Path("extra.csv").write_text("a,b\\n3,4\\n", encoding="utf-8")
            """
        ),
        code("!ls"),
        code("!cat {filename}"),
        code(
            """
            files = !ls *.csv
            print(files)
            """
        ),
    ],
    "08_display_html.ipynb": [
        markdown("# HTML display"),
        code(
            """
            from IPython.display import display, HTML

            display(HTML("<h3>Report</h3><p><b>Hello</b> from generated HTML.</p>"))
            """
        ),
    ],
    "09_display_dataframe.ipynb": [
        markdown("# DataFrame display"),
        code(
            """
            import pandas as pd
            from IPython.display import display

            df = pd.DataFrame({"city": ["Vienna", "Graz"], "value": [10, 20]})
            display(df)
            """
        ),
    ],
    "10_widgets_slider_dropdown.ipynb": [
        markdown("# Widgets: slider, dropdown, and dependent output"),
        code(
            """
            import ipywidgets as widgets
            from IPython.display import display

            slider = widgets.IntSlider(value=3, min=1, max=10, description="Factor")
            dropdown = widgets.Dropdown(
                options=["small", "medium", "large"],
                value="medium",
                description="Size:",
            )

            display(slider)
            display(dropdown)
            """
        ),
        code(
            """
            result = slider.value * 2
            print("selection:", dropdown.value)
            print("result:", result)
            """
        ),
    ],
    "11_interact_widget.ipynb": [
        markdown("# interact widget"),
        code(
            """
            from ipywidgets import interact

            def square(x):
                return x * x

            interact(square, x=(1, 10))
            """
        ),
    ],
    "12_get_ipython_magic.ipynb": [
        markdown("# get_ipython magic call"),
        code(
            """
            get_ipython().run_line_magic("matplotlib", "inline")
            """
        ),
        code(
            """
            import matplotlib.pyplot as plt

            plt.plot([1, 2, 3], [1, 4, 9])
            plt.show()
            """
        ),
    ],
    "13_variable_redefinition.ipynb": [
        markdown("# Variable redefinition across cells"),
        code(
            """
            x = 1
            print("first value:", x)
            """
        ),
        code(
            """
            x = 2
            print("second value:", x)
            """
        ),
    ],
    "14_sales_analysis_widgets_plots.ipynb": [
        markdown(
            """
            # Explorative sales analysis

            This larger notebook creates synthetic sales data, filters it with
            widgets, and shows grouped tables and plots.
            """
        ),
        code("%matplotlib inline"),
        code(
            """
            import pandas as pd
            import matplotlib.pyplot as plt
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
            """
        ),
        markdown(
            """
            ## Interactive filter setup

            The next cells create controls for selecting a region and a minimum
            revenue. The filtered data should update the summary used for the
            chart.
            """
        ),
        code(
            """
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
            """
        ),
        markdown(
            """
            ## Aggregated sales summary

            This step groups the filtered rows by category and compares average
            revenue with average profit.
            """
        ),
        code(
            """
            filtered = sales[sales["revenue"] >= min_revenue.value]
            if region_dropdown.value != "all":
                filtered = filtered[filtered["region"] == region_dropdown.value]

            summary = filtered.groupby("category")[["revenue", "profit"]].mean()
            display(summary)
            """
        ),
        markdown(
            """
            ## Profit chart

            The final chart should make it easy to compare which category has the
            highest average profit after filtering.
            """
        ),
        code(
            """
            %%time
            ax = summary["profit"].plot(kind="bar", title="Average profit by category")
            ax.set_ylabel("profit")
            plt.show()
            """
        ),
    ],
    "15_combined_jupyter_features.ipynb": [
        markdown(
            """
            # Combined Jupyter feature report

            This notebook intentionally combines several Jupyter-specific
            features in one larger workflow: magics, shell commands, generated
            files, captured shell output, widgets, rich display, timing, and
            plots.
            """
        ),
        code(
            """
            get_ipython().run_line_magic("matplotlib", "inline")
            """
        ),
        code("%cd ."),
        markdown(
            """
            ## Imports and report configuration

            The next cell defines reusable report settings and imports the
            libraries used throughout the notebook.
            """
        ),
        code(
            """
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
            """
        ),
        markdown(
            """
            ## Generate report notes

            The next cell writes a small text file with Jupyter's writefile
            magic.
            """
        ),
        code(
            """
            %%writefile report_notes.txt
            Generated report notes
            ======================
            This file was written from a Jupyter cell.
            """
        ),
        markdown(
            """
            ## Create synthetic report data

            The CSV file is generated inside the notebook. No external input file
            is required.
            """
        ),
        code(
            """
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
            """
        ),
        markdown(
            """
            ## Inspect generated files with shell commands

            These cells intentionally use Jupyter shell syntax and captured shell
            output.
            """
        ),
        code("!ls"),
        code("!cat {filename}"),
        code(
            """
            files = !ls *.csv
            print("csv files:", files)
            """
        ),
        markdown(
            """
            ## Read files back into Python

            The generated CSV and text note are loaded again for the report.
            """
        ),
        code(
            """
            data = pd.read_csv(filename)
            notes = Path(notes_file).read_text(encoding="utf-8")
            print(notes)
            display(data.head(10))
            """
        ),
        markdown(
            """
            ## Interactive filters

            These widgets control which rows are included in the summary.
            """
        ),
        code(
            """
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
            """
        ),
        markdown(
            """
            ## Filter and summarize data

            The filtered result depends on both widget values.
            """
        ),
        code(
            """
            filtered = data[data["profit"] >= min_profit_widget.value]
            if region_widget.value != "all":
                filtered = filtered[filtered["region"] == region_widget.value]

            summary = filtered.groupby("category")[["value", "cost", "profit"]].mean()
            display(summary)
            """
        ),
        code(
            """
            %timeit data["value"].sum()
            """
        ),
        markdown(
            """
            ## Timed report calculation

            This cell uses a cell magic around a small aggregate calculation.
            """
        ),
        code(
            """
            %%time
            total_value = filtered["value"].sum()
            total_profit = filtered["profit"].sum()
            print("total value:", total_value)
            print("total profit:", total_profit)
            """
        ),
        markdown(
            """
            ## Rich HTML report

            The report combines values computed in earlier cells.
            """
        ),
        code(
            """
            display(HTML(
                f"<h2>{report_title}</h2>"
                f"<p>Rows after filtering: <b>{len(filtered)}</b></p>"
                f"<p>Total value: <b>{total_value}</b></p>"
                f"<p>Total profit: <b>{total_profit}</b></p>"
            ))
            """
        ),
        markdown(
            """
            ## Plot results

            The final charts should make the category-level differences visible.
            """
        ),
        code(
            """
            ax = summary["profit"].plot(kind="bar", title="Average profit by category")
            ax.set_ylabel("profit")
            plt.show()
            """
        ),
        code(
            """
            fig, ax = plt.subplots()
            ax.scatter(filtered["value"], filtered["profit"], alpha=0.7)
            ax.set_xlabel("value")
            ax.set_ylabel("profit")
            ax.set_title("Value vs profit")
            plt.show()
            """
        ),
    ],
}


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for filename, cells in NOTEBOOKS.items():
        path = OUTPUT_DIR / filename
        path.write_text(
            json.dumps(notebook(cells), indent=2, ensure_ascii=True),
            encoding="utf-8",
        )
        print(f"Created {path}")


if __name__ == "__main__":
    main()
