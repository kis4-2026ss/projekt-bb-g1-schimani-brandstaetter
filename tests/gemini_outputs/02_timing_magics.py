import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md("# Timing magics"),


@app.cell
def _cell_1():
    import timeit
    x = 10
    _timeit_result = timeit.timeit('x = 10', number=1000000)
    print(_timeit_result)
    return x, _timeit_result


@app.cell
def _cell_2():
    import time

    # The IPython magic definition and registration are Jupyter-specific
    # and cannot be directly translated to Marimo.
    # We will execute the code that was originally contained within
    # and after the magic definition, explicitly performing the timing
    # where %%time was implied.

    # This section corresponds to "The original cell content starts here"
    _total_1 = sum(range(100000))
    print(_total_1)

    # This section simulates the execution of the %%time cell magic
    _start_time = time.time()
    _total_2 = sum(range(100000))
    _end_time = time.time()
    _duration = _end_time - _start_time
    print(_total_2)
    print(f"{_duration:.6f} seconds")

    return _duration, _total_1, _total_2