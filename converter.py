import os
import ast
import nbformat
from dotenv import load_dotenv
from google import genai

load_dotenv(".env")

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def fix_with_ai(code):
    # Wir benutzen exakt den Namen aus deiner Liste:
    response = client.models.generate_content(
        model="gemini-3.5-flash", 
        contents=f"Konvertiere diesen Jupyter-Zellinhalt in sauberen Python-Code. Gib NUR den Code zurück:\n{code}",
    )
    return response.text

def analyze_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            code = cell.source
            print(f"\n--- Zelle {i} Analyse ---")
            
            # ist code valides python?
            try:
                tree = ast.parse(code)
                print("Status: Valider Python-Code")
                
                #  variablennamen extrahieren
                nodes = [node for node in ast.walk(tree) if isinstance(node, ast.Name)]
                vars = set(node.id for node in nodes)
                print(f"Verwendete Variablen/Funktionen: {vars}")
                
            except SyntaxError:
                print("Status: Enthält Jupyter-Magics oder ungültiges Python (-> Fall für das LLM!)")
                
                print("... sende an Gemini zur Normalisierung ...")
                fixed_code = fix_with_ai(code)
                print(f"Ergebnis der KI: \n{fixed_code}")
                

analyze_notebook('test.ipynb')