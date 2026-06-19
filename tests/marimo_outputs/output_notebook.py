import marimo as mo
import timeit

app = mo.App()

@app.cell
def _cell_0():
    x = 10
    _timeit_result = timeit.timeit('x = 10', number=1000000)
    print(_timeit_result)
    return x, _timeit_result

@app.cell
def _cell_1():
    print("Hallo Welt")
    return

@app.cell
def __(_cell_0_x):
    print(_cell_0_x)
    return

if __name__ == "__main__":
    app.run()