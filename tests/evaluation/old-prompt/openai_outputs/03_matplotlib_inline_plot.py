import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# Matplotlib inline plot"),

@app.cell
def _cell_1():
    import matplotlib.pyplot as plt
    values = [1, 4, 9, 16]
    plt.plot(values, marker="o")
    plt.title("Square values")
    plt.show()
    return plt, values,