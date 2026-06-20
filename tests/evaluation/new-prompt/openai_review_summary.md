# OpenAI Test Review - New Prompt

Review date: 2026-06-20

This is a static code review of the OpenAI outputs generated with the updated prompt.

Reviewed folder:

- `tests/evaluation/new-prompt/openai_outputs`

## Result

| Check | Result |
| --- | --- |
| Generated outputs | 15 of 15 |
| Python syntax | 15 of 15 OK |
| Static code review OK | 14 of 15 |
| Static code review problematic | 1 of 15 |
| Source test invalid / platform-dependent | 0 of 15 |

## Static Classification

| Status | Tests |
| --- | --- |
| OK | 01, 02, 03, 04, 05, 06, 07, 08, 09, 10, 11, 12, 13, 14 |
| Problematic | 15 |
| Source test invalid / platform-dependent | none |

## Test-by-Test

| Test | Result | Reason |
| --- | --- | --- |
| 01 | OK | Basic Python dependencies are preserved. Imports, function, DataFrame, and dependent cell parameters look correct. |
| 02 | OK | `%timeit` and `%%time` are converted to normal Python timing code. |
| 03 | OK | Plot code is converted to regular Matplotlib figure/axis logic. No Jupyter magic remains. |
| 04 | OK | CSV write/read is preserved and a `file_written` sentinel enforces ordering. |
| 05 | OK | `%%bash` is represented as WSL/Linux shell execution, which matches the Linux-specific source notebook. |
| 06 | OK | `%%writefile` is converted to normal file writing and reading, with `file_written` ordering. |
| 07 | OK with WSL/Linux caveat | The original notebook uses Linux shell commands, so keeping `ls`/`ls *.csv` through `subprocess` is acceptable when the test is run in WSL/Linux. The extra empty dependency cell is unnecessary but not a functional failure. |
| 08 | OK | `display(HTML(...))` is converted to `mo.Html(...)`; no IPython display remains. |
| 09 | OK | DataFrame display no longer uses `IPython.display`; DataFrame is preserved as cell output. |
| 10 | OK | `ipywidgets` are converted to `mo.ui.slider` and `mo.ui.dropdown`; dependent result uses `.value`. |
| 11 | OK | `ipywidgets.interact` is converted to `mo.ui.slider` plus a dependent output cell. |
| 12 | OK | `get_ipython()` is removed; plot is represented as Matplotlib figure logic. |
| 13 | OK | Duplicate public `x` definitions are avoided. It uses a mutable wrapper, which is unusual but statically valid and avoids Marimo duplicate-definition errors. |
| 14 | OK | Uses `mo.ui` widgets, normal pandas/Matplotlib code, and no IPython display. Dummy `display = None` / `widgets = None` are unnecessary but not breaking. |
| 15 | Problematic | Linux shell behavior itself is acceptable because it comes from the original notebook. The remaining issue is the file dependency around `report_data.csv`: a later cell can try to read the file before Marimo has reliably created it in the active working directory. |

## Summary

The new prompt is clearly better than the old prompt. The strongest improvements are:

- Marimo import-cell pattern is used.
- `get_ipython()` is removed in focused tests.
- `display(HTML(...))` becomes `mo.Html(...)`.
- `ipywidgets` becomes `mo.ui` in the focused widget tests.
- File-writing cells often return sentinel variables for ordering.

The remaining clear failure area is not Linux shell usage itself. Linux-specific shell commands are acceptable when they come from the original notebook and the tests are run in WSL/Linux. Test 15 remains problematic because of the `report_data.csv` file dependency/working-directory issue, not because it uses shell commands.
