# OpenAI Test Review - Old Prompt

Review date: 2026-06-20

This is a static code review of the OpenAI outputs generated with the old prompt.

Reviewed folder:

- `tests/evaluation/old-prompt/openai_outputs`

## Result

| Check | Result |
| --- | --- |
| Generated outputs | 15 of 15 |
| Python syntax | 15 of 15 OK |
| Static code review OK | 6 of 15 |
| Static code review problematic | 9 of 15 |
| Source test invalid / platform-dependent | 0 of 15 |

## Static Classification

| Status | Tests |
| --- | --- |
| OK | 01, 02, 03, 04, 05, 06 |
| Problematic | 07, 08, 09, 10, 11, 12, 13, 14, 15 |
| Source test invalid / platform-dependent | none |

## Test-by-Test

| Test | Result | Reason |
| --- | --- | --- |
| 01 | OK | Basic Python imports, function, DataFrame creation, path printing, and data flow are preserved. Some returns are mechanical but acceptable. |
| 02 | OK | `%timeit` and `%%time` are converted to normal Python timing code. Not an exact Jupyter timing reproduction, but the core behavior is present. |
| 03 | OK | Plot code is preserved, `%matplotlib inline` is removed, and the cell calls `plt.show()`. No Jupyter-only plot magic remains. |
| 04 | OK | CSV generation, `os.chdir(".")`, and CSV reading are preserved. The read cell depends on `pd` from the writer cell, so ordering should be acceptable. |
| 05 | OK | `%%bash` is represented as WSL/Linux shell execution, which matches the Linux-specific source notebook. |
| 06 | OK | `%%writefile` became normal file writing and the read cell prints the file content. The file side effect is preserved statically. |
| 07 | Problematic | The failure is not the Linux `ls` command, because that behavior comes from the original notebook and is acceptable in WSL/Linux. The real issue is that the output directly calls decorated cell functions at the bottom (`_cell_0()`, `_cell_1()`, etc.), which violates Marimo's execution model, and `_cell_2` has an artificial `os_import` argument with no real provider. |
| 08 | Problematic | The HTML output was not converted to Marimo-native HTML/Markdown. It still imports `IPython.display` and calls `display(HTML(...))`. |
| 09 | Problematic | The DataFrame is created, but display is still done with `IPython.display.display`. A Marimo conversion should return the DataFrame or use a Marimo-native display mechanism. |
| 10 | Problematic | `ipywidgets` slider/dropdown are left unchanged. This is not Marimo-native and likely does not provide the intended interaction. |
| 11 | Problematic | `ipywidgets.interact(...)` is left unchanged. It should be converted to `mo.ui.slider` plus a dependent output cell. |
| 12 | Problematic | `get_ipython().run_line_magic("matplotlib", "inline")` is still present. In Marimo or normal Python this can raise `NameError`. |
| 13 | Problematic | `x` is returned from multiple cells, so Marimo will likely detect multiple public definitions of `x`. |
| 14 | Problematic | The output keeps `ipywidgets` and `IPython.display`. More importantly, `_cell_1(plt)` requires `plt` before any cell defines it, so the dependency graph is broken. |
| 15 | Problematic | Several Jupyter/IPython constructs remain: `get_ipython`, `ipywidgets`, `IPython.display`, and `display(HTML(...))`. Linux shell usage from the source notebook is acceptable in WSL/Linux. The real conversion issues are broken dependencies: `Path` and `HTML` are imported but not returned, yet later cells require them. `_cell_11(f)` depends on a closed file handle from the writefile cell instead of using `filename`. |

## Summary

The old OpenAI prompt generated files for all 15 tests and all files are syntactically valid Python, but many outputs are not reliable Marimo conversions. The strongest problems are:

- Jupyter/IPython code is often preserved instead of converted.
- `ipywidgets` is not converted to `mo.ui` in the widget tests.
- `display(...)` and `IPython.display` remain in rich-output tests.
- Some generated files violate Marimo dependency rules or directly call decorated cell functions.
- Linux shell commands are acceptable when they come from the original notebook and the tests are run in WSL/Linux; they are not counted as converter failures by themselves.

Compared with the new prompt, this old prompt is clearly weaker. It covers all files, but it preserves too much Jupyter-specific behavior and misses important Marimo execution rules.
