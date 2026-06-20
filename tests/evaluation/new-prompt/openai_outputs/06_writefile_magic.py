import marimo

app = marimo.App()


@app.cell
def _cell_0():
    import marimo as mo

    return mo,


@app.cell
def _cell_1(mo):
    mo.md(r"""# Writefile magic""")
    return


@app.cell
def _cell_2():
    with open("hello.txt", "w", encoding="utf-8") as _f:
        _f.write("Hello from notebook\n")
    file_written = True
    return file_written,


@app.cell
def _cell_3(file_written):
    if file_written:
        with open("hello.txt", encoding="utf-8") as _file:
            print(_file.read())
    return


if __name__ == "__main__":
    app.run()