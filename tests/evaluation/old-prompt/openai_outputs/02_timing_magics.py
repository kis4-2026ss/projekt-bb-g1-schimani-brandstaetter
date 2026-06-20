import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# Timing magics"),

@app.cell
def _cell_1():
    import timeit
    x = 10
    result = timeit.timeit('x = 10', number=1000000)
    return result,

@app.cell
def _cell_2(result):
    import time
    start_time = time.time()
    total = sum(range(100000))
    end_time = time.time()
    print(total)
    print(f"Elapsed time: {end_time - start_time} seconds")
    return total, start_time, end_time,