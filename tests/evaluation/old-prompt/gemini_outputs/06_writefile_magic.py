import marimo as mo

app = mo.App()


@app.cell
def _cell_0():
    return mo.md(
        """
        # Writefile magic
        """
    )


@app.cell
def _cell_1():
    with open("hello.txt", "w") as f:
        f.write("Hello from notebook\n")
    return


@app.cell
def _cell_2():
    with open("hello.txt", encoding="utf-8") as file:
        print(file.read())
    return