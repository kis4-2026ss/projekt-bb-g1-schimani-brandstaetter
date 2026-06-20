# Evaluation Results (openai)

Generated: 2026-06-20T22:35:09

| Test | Notebook | Conversion | Python | Shape | Manual | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 01_basic_python_imports_functions.ipynb | PASS | PASS | PASS | NO | AUTO_PASS |  |
| 2 | 02_timing_magics.ipynb | PASS | PASS | PASS | NO | AUTO_PASS |  |
| 3 | 03_matplotlib_inline_plot.ipynb | PASS | PASS | PASS | YES | MANUAL_REVIEW | plot output should be visually checked |
| 4 | 04_cd_with_generated_csv.ipynb | PASS | PASS | PASS | NO | AUTO_PASS |  |
| 5 | 05_bash_cell_magic.ipynb | PASS | PASS | PASS | NO | AUTO_PASS |  |
| 6 | 06_writefile_magic.ipynb | PASS | PASS | PASS | NO | AUTO_PASS |  |
| 7 | 07_shell_commands_variables_capture.ipynb | PASS | PASS | PASS | NO | AUTO_PASS |  |
| 8 | 08_display_html.ipynb | PASS | PASS | PASS | YES | MANUAL_REVIEW | HTML display should be visually checked |
| 9 | 09_display_dataframe.ipynb | PASS | PASS | PASS | YES | MANUAL_REVIEW | DataFrame display should be checked in Marimo |
| 10 | 10_widgets_slider_dropdown.ipynb | PASS | PASS | PASS | YES | MANUAL_REVIEW | widgets require manual interaction check |
| 11 | 11_interact_widget.ipynb | PASS | PASS | PASS | YES | MANUAL_REVIEW | interact widget requires manual interaction check |
| 12 | 12_get_ipython_magic.ipynb | PASS | PASS | PASS | NO | AUTO_PASS |  |
| 13 | 13_variable_redefinition.ipynb | PASS | PASS | PASS | YES | MANUAL_REVIEW | variable redefinition is a semantic Marimo/Jupyter difference |
| 14 | 14_sales_analysis_widgets_plots.ipynb | PASS | PASS | PASS | YES | MANUAL_REVIEW | large notebook with widgets, tables, and plots needs manual review |
| 15 | 15_combined_jupyter_features.ipynb | PASS | PASS | PASS | YES | MANUAL_REVIEW | large combined Jupyter-feature notebook needs manual review |

## Status meaning

- `AUTO_PASS`: automatic checks passed and no mandatory manual review is marked.
- `MANUAL_REVIEW`: automatic checks passed, but visual/interactive/semantic review is needed.
- `AUTO_FAIL`: conversion or automatic checks failed.
- `STOPPED_QUOTA`: token/quota/rate-limit condition detected; following tests were skipped.
