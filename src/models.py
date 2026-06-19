from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class NotebookCell:
    index: int
    cell_type: str
    source: str
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_code(self) -> bool:
        return self.cell_type == "code"

    @property
    def is_markdown(self) -> bool:
        return self.cell_type == "markdown"


@dataclass(frozen=True)
class CodeCellAnalysis:
    cell: NotebookCell
    defined: set[str]
    used: set[str]
    imports: list[str]
    functions: list[str]
    classes: list[str]

    @property
    def cell_index(self) -> int:
        return self.cell.index


@dataclass(frozen=True)
class DependencyEdge:
    source: int
    target: int
    variables: tuple[str, ...]


@dataclass
class DependencyGraph:
    nodes: dict[int, CodeCellAnalysis] = field(default_factory=dict)
    dependency_edges: list[DependencyEdge] = field(default_factory=list)

    def add_node(self, cell_index: int, analysis: CodeCellAnalysis) -> None:
        self.nodes[cell_index] = analysis

    def add_edge(self, source: int, target: int, variables: tuple[str, ...]) -> None:
        self.dependency_edges.append(
            DependencyEdge(source=source, target=target, variables=variables)
        )

    def number_of_nodes(self) -> int:
        return len(self.nodes)

    def number_of_edges(self) -> int:
        return len(self.dependency_edges)


@dataclass(frozen=True)
class ParsedNotebook:
    cells: list[NotebookCell]

    @property
    def code_cells(self) -> list[NotebookCell]:
        return [cell for cell in self.cells if cell.is_code]
