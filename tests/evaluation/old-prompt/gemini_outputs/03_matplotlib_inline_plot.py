import marimo as mo
app = mo.App()


@app.cell
def _cell_0():
    return mo.md(
        """
        # Matplotlib inline plot
        """
    )


@app.cell
def _cell_1():
    import matplotlib.pyplot as plt
    import subprocess

    # Simulate %matplotlib inline - this is implicitly handled by plt.show() in many environments
    # and doesn't require explicit Python code for basic plotting.
    # If explicit inline display is needed in certain contexts (like saving to a file without plt.show()),
    # you might use backend configurations, but for general execution, it's often not needed.

    values = [1, 4, 9, 16]
    plt.plot(values, marker="o")
    plt.title("Square values")
    plt.show()
    return plt, subprocess, values