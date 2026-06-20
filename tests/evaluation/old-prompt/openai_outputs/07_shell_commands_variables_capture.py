import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# Shell commands with variables and captured output"),

@app.cell
def _cell_1():
    from pathlib import Path
    filename = "data.csv"
    Path(filename).write_text("a,b\n1,2\n", encoding="utf-8")
    Path("extra.csv").write_text("a,b\n3,4\n", encoding="utf-8")
    return filename, 

@app.cell
def _cell_2(os_import):
    import os
    os.system('ls')
    return

@app.cell
def _cell_3(filename):
    with open(filename, 'r') as file:
        content = file.read()
        print(content)
    return content, 

@app.cell
def _cell_4():
    import glob
    files = glob.glob('*.csv')
    print(files)
    return files, 

_cell_0()
filename = _cell_1()[0]
_cell_2(None)
content = _cell_3(filename)[0]
files = _cell_4()[0]