from __future__ import annotations

import ast
import builtins

from models import CodeCellAnalysis, NotebookCell

BUILTINS = set(dir(builtins))

class AstParser:
    def validate_python(self, code: str) -> bool:
        try:
            ast.parse(code)
        except SyntaxError:
            return False

        return True

    def validate_marimo_output(self, code: str) -> None:
        error = self.check_marimo_output(code)

        if error:
            raise RuntimeError(error)

    def check_marimo_output(self, code: str) -> str | None:
        try:
            ast.parse(code)
        except SyntaxError as exc:
            return f"Generated Marimo notebook is invalid Python:\n{exc}"

        return None

    def analyze_code_cell(self, cell: NotebookCell) -> CodeCellAnalysis:
        if not cell.is_code:
            raise ValueError("Only code cells can be analyzed with the AST parser.")

        tree = ast.parse(cell.source)

        return CodeCellAnalysis(
            cell=cell,
            defined=self._extract_defined(tree),
            used=self._extract_used(tree),
            imports=self._extract_imports(tree),
            functions=self._extract_functions(tree),
            classes=self._extract_classes(tree),
        )

    def _extract_defined(self, tree: ast.AST) -> set[str]:
        defined = {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)
        }

        defined.update(self._extract_functions(tree))
        defined.update(self._extract_classes(tree))
        defined.update(self._extract_imported_names(tree))

        return defined

    def _extract_used(self, tree: ast.AST) -> set[str]:
        return {
            node.id
            for node in ast.walk(tree)
            if isinstance(node, ast.Name) 
            and isinstance(node.ctx, ast.Load)
            and node.id not in BUILTINS
        }

    def _extract_imports(self, tree: ast.AST) -> list[str]:
        imports = []

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                imports.extend(f"{module}.{alias.name}" for alias in node.names)

        return imports

    def _extract_imported_names(self, tree: ast.AST) -> set[str]:
        imported_names = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    imported_names.add(alias.asname or alias.name)

        return imported_names

    def _extract_functions(self, tree: ast.AST) -> list[str]:
        return [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

    def _extract_classes(self, tree: ast.AST) -> list[str]:
        return [
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

