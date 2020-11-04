import metagraph as mg
from metagraph import concrete_algorithm
from .. import has_karateclub
from typing import Tuple

if has_karateclub:
    import karateclub
    import numpy as np
    import networkx as nx
    from metagraph.plugins.networkx.types import NetworkXGraph
    from metagraph.plugins.numpy.types import (
        NumpyMatrix,
        NumpyNodeMap,
    )

    @concrete_algorithm("embedding.train.node2vec")
    def karateclub_node2vec_train(
        graph: NetworkXGraph,
        p: float,
        q: float,
        walks_per_node: int,
        walk_length: int,
        embedding_size: int,
        epochs: int,
        learning_rate: float,
        worker_count: int = 1,
    ) -> Tuple[NumpyMatrix, NumpyNodeMap]:
        trainer = karateclub.Node2Vec(
            walk_number=walks_per_node,
            walk_length=walk_length,
            workers=worker_count,
            p=p,
            q=q,
            dimensions=embedding_size,
            epochs=epochs,
            learning_rate=learning_rate,
        )
        old2canonical = {
            node: canonical_index
            for canonical_index, node in enumerate(sorted(graph.value.nodes))
        }
        relabelled_graph = nx.relabel_nodes(graph.value, old2canonical, copy=True)
        trainer.fit(relabelled_graph)
        np_embedding_matrix = trainer.get_embedding()
        matrix = NumpyMatrix(np_embedding_matrix)
        node2index = NumpyNodeMap(
            np.arange(len(graph.value.nodes)), node_ids=old2canonical
        )
        return (matrix, node2index)

    @concrete_algorithm("embedding.train.graph2vec")
    def karateclub_graph2vec_train(
        graphs: mg.List[NetworkXGraph],
        subgraph_degree: int,
        embedding_size: int,
        epochs: int,
        learning_rate: float,
        worker_count: int = 1,
    ) -> NumpyMatrix:
        if not all(nx.is_connected(graph.value) for graph in graphs):
            raise ValueError("Graphs must be connected")
        graph2vec_trainer = karateclub.Graph2Vec(
            wl_iterations=subgraph_degree,
            dimensions=embedding_size,
            workers=worker_count,
            epochs=epochs,
            learning_rate=learning_rate,
            min_count=0,
        )
        graph2vec_trainer.fit(
            [
                nx.relabel_nodes(
                    graph.value,
                    dict(map(reversed, enumerate(graph.value.nodes))),
                    copy=True,
                )
                for graph in graphs
            ]
        )
        np_embedding_matrix = graph2vec_trainer.get_embedding()
        matrix = NumpyMatrix(np_embedding_matrix)
        return matrix
