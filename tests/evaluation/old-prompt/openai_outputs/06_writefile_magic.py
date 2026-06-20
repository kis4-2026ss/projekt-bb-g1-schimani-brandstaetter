import marimo as mo
app = mo.App()

@app.cell
def _cell_0():
    return

@app.cell
def _cell_1():
    with open('hello.txt', 'w') as f:
        f.write('Hello from notebook')
    return f,

@app.cell
def _cell_2(f):
    with open("hello.txt", encoding="utf-8") as file:
        print(file.read())
    return file,