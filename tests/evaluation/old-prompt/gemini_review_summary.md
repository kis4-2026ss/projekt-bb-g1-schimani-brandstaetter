# Gemini Test Review - Old Prompt

Review date: 2026-06-20

This is a static code review of the Gemini outputs generated with the old prompt.

Reviewed folder:

- `tests/evaluation/old-prompt/gemini_outputs`

## Result

| Check | Result |
| --- | --- |
| Generated outputs | 13 of 15 |
| Python syntax | 13 of 13 OK |
| Static code review OK | 10 of 15 |
| Static code review problematic | 5 of 15 |
| Source test invalid / platform-dependent | 0 of 15 |

## Static Classification

| Status | Tests |
| --- | --- |
| OK | 01, 02, 03, 04, 05, 06, 07, 09, 12, 13 |
| Problematic | 08, 10, 11, 14, 15 |
| Source test invalid / platform-dependent | none |

## Test-by-Test

| Test | Result | Reason |
| --- | --- | --- |
| 01 | OK | Basic imports, function definition, variable flow, DataFrame creation, and prints are preserved. Returning `pd` and `Path` is mechanical but supports downstream dependencies. |
| 02 | OK with caveat | `%timeit` and `%%time` are converted into normal Python timing code. The result is not a perfect Jupyter timing reproduction, but the intended behavior is present. |
| 03 | OK | Plot code is preserved, `%matplotlib inline` is removed, and the cell calls `plt.show()`. No Jupyter-only plot magic remains. |
| 04 | OK | CSV generation, `%cd .`, and CSV reading are preserved. `os.chdir(".")` is harmless. The read cell depends on `pd`, so the CSV-producing cell should run before it. |
| 05 | OK | `%%bash` is represented as WSL/Linux shell execution, which matches the Linux-specific source notebook. |
| 06 | OK | The `%%writefile` behavior is converted to normal file writing, and the read cell prints the file. The file side effect is preserved statically. |
| 07 | OK with WSL/Linux caveat | The original notebook uses Linux shell commands, so `ls` and `cat` behavior is acceptable when the test is run in WSL/Linux. The captured output is simplified to `os.listdir`; this is not identical to shell capture, but the intended CSV listing behavior is preserved. |
| 08 | Problematic | The generated file dropped the actual HTML output. It contains comments explaining `display(HTML(...))`, but returns nothing. The original visible report is lost. |
| 09 | OK | The DataFrame is created and returned from the cell, so the tabular output is preserved in Marimo's dataflow model. `pd` is returned unnecessarily and comments are noisy, but the core behavior is present. |
| 10 | Problematic | `ipywidgets` slider/dropdown were converted into Marimo UI elements, but the generated dependencies do not preserve the intended interactive behavior correctly. |
| 11 | Problematic | Gemini left `ipywidgets.interact(...)` mostly unchanged and only added comments saying Marimo-native UI would be better. This does not satisfy the conversion goal. |
| 12 | OK | `get_ipython().run_line_magic("matplotlib", "inline")` was neutralized, the plot code is preserved, and the cell calls `plt.show()`. No `get_ipython()` runtime dependency remains. |
| 13 | OK with semantic caveat | The original notebook redefines `x` across cells. Gemini avoided Marimo duplicate-definition errors by renaming to `x_from_cell1` and `x_from_cell2`. The printed output is preserved, but the exact global-name behavior differs. |
| 14 | Problematic | No output file exists. The log says: `LLM produced invalid Python in cell 1`. |
| 15 | Problematic | No output file exists. Conversion stopped because Gemini free-tier quota was exhausted with `429 RESOURCE_EXHAUSTED`. |

## Summary

The old Gemini prompt produced acceptable results for many focused tests, but it failed or stopped on the larger notebooks. The strongest problems are:

- HTML display can be lost completely, as seen in test 08.
- `ipywidgets.interact` is not converted to a Marimo-native UI pattern.
- Some outputs contain explanatory comments instead of clean converted behavior.
- Tests 14 and 15 were not successfully generated.
- Linux shell commands are acceptable when they come from the original notebook and the tests are run in WSL/Linux; they are not counted as converter failures by themselves.

Compared with the new OpenAI prompt result, this old Gemini run is less complete because two outputs are missing. It still handled some focused Python and display cases reasonably well, but the bigger notebooks and widget/display conversions remain the main weak spots.
