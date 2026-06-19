import marimo
app = marimo.App()

@app.cell
def _():
    # [FEHLER: KI-Reparatur fehlgeschlagen: Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}]
    %timeit x = 10
    return

@app.cell
def _():
    print("Hallo Welt")
    return

@app.cell
def _():
    print(x)
    return

if __name__ == '__main__':
    app.run()