import marimo as mo

app = mo.App()

@app.cell
def _cell_0():
    return mo.md("# Timing magics")

@app.cell
def _cell_1():
    from timeit import timeit
    x = 10
    setup_code = "x = 10"
    stmt = "x = 10"
    result = timeit(stmt, setup=setup_code, number=100000)
    print(f"{result:.6f} seconds per loop (mean of {100000} loops)")
    return

@app.cell
def _cell_2():
    # The original notebook cell defined and registered an IPython magic.
    # Marimo does not operate within an IPython environment in the same way,
    # and direct translation of `get_ipython()` and magic registration
    # would lead to errors in Marimo.
    # To preserve the *behavior* and *intent* of the original cell (which was
    # to time a piece of code), we directly apply the timing logic
    # to the code that the magic would have executed.
    import time

    # Simulate the code that would have been passed to the `cell_magic`'s `cell` argument
    _start_time = time.time()
    total = sum(range(100000))
    print(total)
    _end_time = time.time()

    print(f"CPU times: user: {_end_time - _start_time:.4f} s, real: {_end_time - _start_time:.4f} s")
    return