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
        try:
            tree = ast.parse(code)
        except SyntaxError as exc:
            raise RuntimeError(f"Generated Marimo notebook is invalid:\n{exc}") from exc

        self._validate_app_run(tree)
        self._validate_marimo_cell_semantics(tree)

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

    def _validate_marimo_cell_semantics(self, tree: ast.AST) -> None:
        cell_functions = [
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef) and self._is_marimo_cell(node)
        ]
        self._validate_unique_cell_function_names(cell_functions)
        cell_function_names = {node.name for node in cell_functions}
        definitions_by_name: dict[str, list[str]] = {}

        for cell_function in cell_functions:
            for assigned_name in self._public_assigned_names(cell_function):
                definitions_by_name.setdefault(assigned_name, []).append(cell_function.name)

            for call in ast.walk(cell_function):
                if (
                    isinstance(call, ast.Call)
                    and isinstance(call.func, ast.Name)
                    and call.func.id in cell_function_names
                ):
                    raise RuntimeError(
                        "Generated Marimo notebook calls a decorated cell function "
                        f"directly: `{call.func.id}()`."
                    )

        duplicate_names = {
            name: functions
            for name, functions in definitions_by_name.items()
            if len(functions) > 1
        }

        if duplicate_names:
            details = ", ".join(
                f"`{name}` in {functions}" for name, functions in duplicate_names.items()
            )
            raise RuntimeError(
                "Generated Marimo notebook defines public variables in multiple cells: "
                f"{details}."
            )

    def _validate_app_run(self, tree: ast.AST) -> None:
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and isinstance(node.func.value, ast.Name)
                and node.func.value.id == "app"
                and node.func.attr == "run"
            ):
                return

        raise RuntimeError("Generated Marimo notebook is missing `app.run()`.")

    def _validate_unique_cell_function_names(
        self,
        cell_functions: list[ast.FunctionDef],
    ) -> None:
        seen = set()
        duplicates = set()

        for cell_function in cell_functions:
            if cell_function.name in seen:
                duplicates.add(cell_function.name)

            seen.add(cell_function.name)

        if duplicates:
            duplicate_list = ", ".join(f"`{name}`" for name in sorted(duplicates))
            raise RuntimeError(
                "Generated Marimo notebook uses duplicate cell function names: "
                f"{duplicate_list}."
            )

    def _is_marimo_cell(self, node: ast.FunctionDef) -> bool:
        for decorator in node.decorator_list:
            if (
                isinstance(decorator, ast.Attribute)
                and isinstance(decorator.value, ast.Name)
                and decorator.value.id == "app"
                and decorator.attr == "cell"
            ):
                return True

            if (
                isinstance(decorator, ast.Call)
                and isinstance(decorator.func, ast.Attribute)
                and isinstance(decorator.func.value, ast.Name)
                and decorator.func.value.id == "app"
                and decorator.func.attr == "cell"
            ):
                return True

        return False

    def _public_assigned_names(self, node: ast.FunctionDef) -> set[str]:
        return {
            name
            for child in ast.walk(node)
            for name in self._assigned_names(child)
            if not name.startswith("_")
        }

    def _assigned_names(self, node: ast.AST) -> set[str]:
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            return {node.id}

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return {node.name}

        return set()
