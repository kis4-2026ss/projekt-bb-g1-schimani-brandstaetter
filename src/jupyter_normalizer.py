from __future__ import annotations

import re


class JupyterNormalizer:
    def normalize(self, code: str) -> str | None:
        stripped = code.strip()

        if stripped.startswith("%timeit "):
            return self._normalize_timeit(stripped)

        if stripped.startswith("%matplotlib"):
            return "# Matplotlib display magic omitted for Marimo compatibility."

        return None

    def _normalize_timeit(self, code: str) -> str:
        statement = code.removeprefix("%timeit").strip()
        assignment = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)", statement)

        if assignment:
            name, value = assignment.groups()
            return (
                "import timeit\n"
                f"{name} = {value}\n"
                f"_timeit_result = timeit.timeit({statement!r}, number=1000000)\n"
                "print(_timeit_result)"
            )

        return (
            "import timeit\n"
            f"_timeit_result = timeit.timeit({statement!r}, number=1000000)\n"
            "print(_timeit_result)"
        )
