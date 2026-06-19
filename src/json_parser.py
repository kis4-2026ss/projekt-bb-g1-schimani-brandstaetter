from __future__ import annotations

import json
from pathlib import Path

from models import NotebookCell, ParsedNotebook


class JsonParser:
    """Reads Jupyter notebook JSON and exposes normalized cell objects."""

    def parse(self, input_file: str | Path) -> ParsedNotebook:
        path = Path(input_file)

        with path.open("r", encoding="utf-8") as notebook_file:
            notebook = json.load(notebook_file)

        cells = [
            NotebookCell(
                index=index,
                cell_type=cell["cell_type"],
                source=self._source_as_text(cell.get("source", "")),
                metadata=dict(cell.get("metadata", {})),
            )
            for index, cell in enumerate(notebook.get("cells", []))
            if cell.get("cell_type") in {"code", "markdown"}
        ]

        return ParsedNotebook(cells=cells)

    def _source_as_text(self, source: str | list[str]) -> str:
        if isinstance(source, list):
            return "".join(source)

        return source
