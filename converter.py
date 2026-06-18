import nbformat

def parse_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    for i, cell in enumerate(nb.cells):
        print(f"--- Zelle {i} (Typ: {cell.cell_type}) ---")
        print(cell.source)
        print("\n")

parse_notebook('test.ipynb')