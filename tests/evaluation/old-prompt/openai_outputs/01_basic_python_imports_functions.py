import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# Basic Python, imports, functions, and data flow"), 

@app.cell
def _cell_1():
    import pandas as pd
    from pathlib import Path
    
    base = 10
    return pd, Path, base,

@app.cell
def _cell_2(pd, base):
    def add_tax(value):
        return value * 1.2
    
    return add_tax,

@app.cell
def _cell_3(pd, Path, base, add_tax):
    df = pd.DataFrame({"value": [base, add_tax(base)]})
    current_path = Path(".")
    print(current_path.resolve())
    print(df)
    return current_path, df,