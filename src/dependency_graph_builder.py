from __future__ import annotations

from models import CodeCellAnalysis, DependencyEdge, DependencyGraph


class DependencyGraphBuilder:
    def build(self, analyzed_cells: list[CodeCellAnalysis]) -> DependencyGraph:
        graph = DependencyGraph()

        for analysis in analyzed_cells:
            graph.add_node(analysis.cell_index, analysis)

        for producer in analyzed_cells:
            if not producer.defined:
                continue

            for consumer in analyzed_cells:
                if producer.cell_index == consumer.cell_index:
                    continue

                variables = tuple(sorted(producer.defined.intersection(consumer.used)))

                if variables:
                    graph.add_edge(
                        producer.cell_index,
                        consumer.cell_index,
                        variables,
                    )

        return graph

    def edges(self, graph: DependencyGraph) -> list[DependencyEdge]:
        return graph.dependency_edges
