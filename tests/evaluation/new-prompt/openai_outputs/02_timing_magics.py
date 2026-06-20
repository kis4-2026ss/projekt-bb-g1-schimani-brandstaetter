import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo
    return mo,


@app.cell
def _cell_1(mo):
    mo.md(r"""# Timing magics""")
    return


@app.cell
def _cell_2():
    import timeit

    print(timeit.timeit("x = 10"))
    return


@app.cell
def _cell_3():
    import time

    _start_cpu_time = time.process_time()
    _start_wall_time = time.perf_counter()

    total = sum(range(100000))
    print(total)

    _end_cpu_time = time.process_time()
    _end_wall_time = time.perf_counter()

    print(f"CPU times: total: {_end_cpu_time - _start_cpu_time:.6f} s")
    print(f"Wall time: {_end_wall_time - _start_wall_time:.6f} s")
    return


if __name__ == "__main__":
    app.run()