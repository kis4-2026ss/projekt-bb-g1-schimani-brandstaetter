import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return 

@app.cell
def _cell_1():
    get_ipython().run_line_magic("matplotlib", "inline")
    return

@app.cell
def _cell_2():
    import matplotlib.pyplot as plt
    _ = plt.plot([1, 2, 3], [1, 4, 9])
    plt.show()
    return