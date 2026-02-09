class ClimateGraph:
    """
    Simple in-memory causal graph.
    """

    def __init__(self):
        self.nodes = []
        self.edges = []

    def build_from_chain(self, chain):

        self.nodes = chain
        self.edges = []

        for i in range(len(chain) - 1):
            self.edges.append((chain[i], chain[i + 1]))

    def to_dict(self):
        return {
            "nodes": self.nodes,
            "edges": self.edges
        }
